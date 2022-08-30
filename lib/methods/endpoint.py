from ast import operator
from contextlib import suppress
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from operator import eq, ge, gt, le, lt, ne
from types import MappingProxyType
from typing import Any, Final, Iterable, List, Optional, Tuple, Type, Union

from dateutil.parser import isoparse
from fastapi.applications import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse
from orjson import loads
from sqlalchemy.ext.asyncio.scoping import async_scoped_session
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.expression import delete, insert, or_, select, update
from sqlalchemy.sql.functions import count, func
from sqlalchemy.sql.schema import Column, MetaData, Table
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_304_NOT_MODIFIED,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from ..middleware.async_sqlalchemy_middleware import ColumnFilter
from ..models.base_interface import Base, BaseInterface

#
OperatorDict: Final[
    MappingProxyType[str, Optional[operator]]
] = MappingProxyType(
    {'>=': ge, '<=': le, '>': gt, '<': lt, '!': ne, '=': eq}
    | {'@@': None, '@>': None}
)
SQLAlhemyMethodDict: Final[
    MappingProxyType[str, Type[Any]]
] = MappingProxyType(
    {'GET': select, 'POST': insert, 'PUT': update, 'DELETE': delete}
)


async def endpoint(request: Request, /) -> Response:
    if not isinstance(app := request.get('app'), FastAPI):
        raise HTTPException(
            HTTP_500_INTERNAL_SERVER_ERROR, 'App is not present.'
        )
    if not isinstance(Session := request.get('Session'), async_scoped_session):
        raise HTTPException(
            HTTP_500_INTERNAL_SERVER_ERROR, 'Session is not present.'
        )
    if not isinstance(metadata := request.get('metadata'), MetaData):
        raise HTTPException(
            HTTP_500_INTERNAL_SERVER_ERROR, 'MetaData is not present.'
        )
    if not isinstance(route := request.path_params.get('route'), str):
        raise HTTPException(
            HTTP_500_INTERNAL_SERVER_ERROR, 'Route is not present.'
        )

    route = route.lower()
    table: Table
    for table_name, table in metadata.tables.items():
        if route == table_name.lower():
            for declarative in Base.registry._class_registry.data.values():
                if declarative.key.startswith('_'):
                    pass
                elif (model := declarative()).__tablename__ == table_name:
                    break
            else:
                model: Optional[Type[BaseInterface]] = None
            break
    else:
        raise HTTPException(HTTP_400_BAD_REQUEST, 'Route is not determined.')

    response: Type[Response] = getattr(
        app.router, 'default_response_class', None
    )
    if response is None:
        response = ORJSONResponse

    query_parameters: dict[str, list[str]] = {}
    for parameter, value in request.query_params._list:
        if (parameter := parameter.lower()) not in query_parameters:
            query_parameters[parameter] = []
        query_parameters[parameter].append(value.lower())

    def get_keys(
        model: Union[Type[BaseInterface], Table],
    ) -> tuple[dict[str, Column], Optional[dict[str, RelationshipProperty]]]:
        return (
            {_.key: _ for _ in model.columns if _.key},
            {_.key: _ for _ in model.relationships if _.key}
            if issubclass(model, BaseInterface)
            else None,
        )

    def get_field(
        model: Union[Type[BaseInterface], Table],
        field: str,
        /,
        field_chain: tuple[str, ...] = (),
        relationship_chain: tuple[RelationshipProperty, ...] = (),
    ):
        column_keys, relationship_keys = get_keys(model)
        field, *relationship_fields = field.split('.')
        if is_relationship := field not in column_keys:
            if relationship_keys is None:
                raise HTTPException(
                    HTTP_500_INTERNAL_SERVER_ERROR,
                    f'Mapper for table "{model.name}" is not present.',
                )
            if field not in relationship_keys:
                raise HTTPException(
                    HTTP_400_BAD_REQUEST,
                    f'Field "{field}" is not present in %s.'
                    % '.'.join((table_name, *field_chain)),
                )

        if is_relationship and relationship_fields:
            for relationship in relationship_keys.values():
                if relationship.key == field:
                    try:
                        return get_field(
                            relationship.entity.class_,
                            '.'.join(relationship_fields),
                            (*field_chain, field),
                            (*relationship_chain, getattr(model, field)),
                        )
                    except AttributeError as _:
                        raise HTTPException(
                            HTTP_500_INTERNAL_SERVER_ERROR,
                            'Could not infer type for relationship: '
                            f'{relationship}',
                        ) from _

            raise HTTPException(
                HTTP_400_BAD_REQUEST,
                f'Relationship "{field}" is not present in %s.'
                % '.'.join((table_name, *field_chain)),
            )
        return (*relationship_chain, getattr(model, field))

    def get_filters() -> Iterable[
        Tuple[
            Tuple[RelationshipProperty],
            Union[Column, InstrumentedAttribute],
            Tuple[ColumnFilter],
        ]
    ]:
        filters: List[
            Tuple[
                Tuple[RelationshipProperty],
                Union[Column, InstrumentedAttribute],
                Tuple[ColumnFilter],
            ]
        ] = []
        for param, values in query_parameters.items():
            try:
                *chain, field = get_field(model or table, param)
            except HTTPException as exception:
                if exception.status_code >= HTTP_500_INTERNAL_SERVER_ERROR:
                    raise
                continue
            field = getattr(field.property, 'expression', field)
            if not isinstance(column := field, Column):
                filters.append((tuple(chain), field, ()))
                continue

            if getattr(getattr(column.type, 'impl', None), 'python_type', ''):
                type = column.type.impl.python_type
            elif getattr(column.type, 'python_type', None):
                type = column.type.python_type
            else:
                raise HTTPException(
                    HTTP_500_INTERNAL_SERVER_ERROR,
                    f'Could not infer python type for {column.key}.',
                )

            column_filters: List[ColumnFilter] = []
            for value in values:
                for op_key, op in OperatorDict.items():
                    if value.startswith(op_key):
                        value = value.removeprefix(op_key)
                    elif value.endswith(op_key):
                        value = value.removesuffix(op_key)
                    else:
                        continue
                    break
                else:
                    op: Optional[operator] = eq

                try:
                    if value == '' and column.nullable:
                        value = None

                    if issubclass(type, bool):
                        if value not in {'true', 'false'}:
                            raise ValueError
                        value = value == 'true'
                    elif issubclass(type, (int, float, Decimal)):
                        value = type(value)
                    elif issubclass(type, timedelta):
                        value = timedelta(seconds=float(value))
                    elif issubclass(type, date):
                        value = isoparse(value).date()
                    elif issubclass(type, time):
                        value = isoparse(value).time()
                    elif issubclass(type, datetime):
                        value = isoparse(value)

                except ValueError as _:
                    raise HTTPException(
                        HTTP_400_BAD_REQUEST,
                        f"Value of type '{value.__class__.__name__}' of "
                        f"parameter '{parameter}' is invalid, should be valid "
                        f"value of type '{type.__name__}'.",
                    ) from _

                column_filters.append((value, op or op_key))
            if column_filters:
                filters.append((tuple(chain), column, tuple(column_filters)))
        return filters

    option: str = request.path_params.get('option', '').lower()
    if request.method == 'DELETE':
        statement = delete(table)
        if option == 'return':
            statement = statement.returning(*table.columns)

        for chain, field, values in get_filters():
            if chain and values:
                parent = next(chain := iter(chain))
                statement = statement.join(parent)
                for parent in chain:
                    statement = statement.join(parent)

            if values:
                statement = statement.where(
                    or_(
                        *(
                            field.op(op)(
                                func.to_tsquery(value) if op == '@@' else value
                            )
                            if isinstance(op, str)
                            else op(field, value)
                            for value, op in values
                        )
                    )
                )

        async with Session.begin():
            result = await Session.execute(statement)

        if option == 'return':
            column_keys: list[str] = [column.key for column in table.columns]
            items = [
                model(**dict(zip(column_keys, item)))
                if model is not None
                else item
                for item in result.fetchall()
            ]
            return response(items)
        return Response(None, HTTP_204_NO_CONTENT)

    elif request.method in {'POST', 'PUT'}:
        if not isinstance(body := loads(await request.body()), Iterable):
            raise HTTPException(HTTP_400_BAD_REQUEST, 'Body is invalid.')
        elif isinstance(body, list) and not body:
            raise HTTPException(HTTP_304_NOT_MODIFIED, 'Body is empty.')

        def modify_item(
            model: Union[Type[BaseInterface], Table],
            item: Union[dict[str, Any], list[dict[str, Any]]],
            /,
            field_chain: tuple[str, ...] = (),
        ) -> dict[str, Any]:
            column_keys, relationship_keys = get_keys(model)
            if isinstance(item, dict):
                item = dict.fromkeys(column_keys) | item
                for field, value in dict(item).items():
                    if field in column_keys:
                        if field in {'created_at', 'updated_at'}:
                            del item[field]
                            continue
                        column = column_keys[field]
                        if (
                            (not field_chain and value is None)
                            and column.default is None
                            and not column.nullable
                            and column.autoincrement is not True
                        ):
                            raise HTTPException(
                                HTTP_400_BAD_REQUEST,
                                'Table `{name}` requires fields: '
                                '{fields}.'.format(
                                    name=model.name
                                    if isinstance(model, Table)
                                    else model.__tablename__,
                                    fields=', '.join(
                                        f'`{column.key}`'
                                        for column in column_keys.values()
                                        if column.default is None
                                        and not column.nullable
                                        and column.autoincrement is not True
                                    ),
                                ),
                            )

                        ctype = None
                        with suppress(NotImplementedError):
                            ctype = column.type.python_type
                        if ctype is None or isinstance(
                            value, (ctype, type(None))
                        ):
                            pass
                        elif ctype == date:
                            item[field] = isoparse(value).date()
                        elif ctype == time:
                            item[field] = isoparse(value).time()
                        elif ctype == datetime:
                            item[field] = isoparse(value)
                        elif ctype == timedelta:
                            if isinstance(value, (int, float)):
                                item[field] = timedelta(seconds=value)
                        continue

                    elif relationship_keys is None:
                        raise HTTPException(
                            HTTP_500_INTERNAL_SERVER_ERROR,
                            f'Mapper for table "{model.name}" is not present.',
                        )
                    elif relationship := relationship_keys.get(field):
                        if not value:
                            del item[field]
                            continue
                        try:
                            item[field] = modify_item(
                                relationship.entity.class_,
                                value,
                                (*field_chain, field),
                            )
                        except AttributeError as _:
                            raise HTTPException(
                                HTTP_500_INTERNAL_SERVER_ERROR,
                                'Could not infer type for relationship: '
                                f'{relationship}',
                            ) from _
                return model(**item)

            elif item:
                items = []
                for index, item in enumerate(item):
                    if not isinstance(item, dict):
                        raise HTTPException(
                            HTTP_400_BAD_REQUEST,
                            f'%s element #{index} should be a dictionary.'
                            % '.'.join((route, *field_chain)),
                        )
                    items.append(modify_item(model, item, field_chain))
                return items

        items = []
        if isinstance(body, dict):
            items.append(modify_item(model or table, body))
        elif isinstance(body, Iterable):
            for item in body:
                items.append(modify_item(model or table, item))

        async with Session.begin():
            if request.method == 'POST':
                for item in items:
                    Session.add(item)
            else:
                items = [await Session.merge(item) for item in items]

        if option == 'return':
            return response(items)
        return Response(None, HTTP_204_NO_CONTENT)

    else:
        statement = select(model or table)
        for chain, field, values in get_filters():
            if values:
                for link in chain:
                    statement = statement.join(link)
                statement = statement.where(
                    or_(
                        *(
                            field.op(op)(
                                func.to_tsquery(value) if op == '@@' else value
                            )
                            if isinstance(op, str)
                            else op(field, value)
                            for value, op in values
                        )
                    )
                )
            else:
                option = selectinload(next(chain := iter((*chain, field))))
                for link in chain:
                    option = option.selectinload(link)
                statement = statement.options(option)

        if 'limit' in query_parameters:
            try:
                statement = statement.limit(int(query_parameters['limit']))
            except ValueError as _:
                raise HTTPException(
                    HTTP_400_BAD_REQUEST, 'Limit is invalid.'
                ) from _

        if 'offset' in query_parameters:
            try:
                statement = statement.offset(int(query_parameters['offset']))
            except ValueError as _:
                raise HTTPException(
                    HTTP_400_BAD_REQUEST, 'Offset is invalid.'
                ) from _

        if option == 'count':
            statement = select(count()).select_from(statement)
            return Response(str(await Session.scalar(statement)))

        if orderings := [
            column.asc() if parameter.startswith('asc') else column.desc()
            for parameter, values in query_parameters.items()
            if parameter in {'asc', 'ascending', 'desc', 'descending'}
            for value in values
            if (column := table.columns.get(value)) is not None
        ]:
            statement = statement.order_by(*orderings)

        async def get_response() -> list:
            nonlocal Session, statement
            if model is None:
                result = await Session.execute(statement)
                return list(map(list, result.unique().all()))
            return (await Session.scalars(statement)).unique().all()

        try:
            return response(await get_response())
        except TypeError as _:
            raise HTTPException(
                HTTP_500_INTERNAL_SERVER_ERROR,
                'Request was valid, but could not process response '
                'correctly.',
            ) from _
