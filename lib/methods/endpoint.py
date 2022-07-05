from ast import operator
from operator import eq, ge, gt, le, lt, ne
from types import MappingProxyType
from typing import Any, Final, Iterable, Optional, Type, Union

from fastapi.applications import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse
from orjson import dumps, loads
from sqlalchemy.ext.asyncio.scoping import async_scoped_session
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.expression import delete, insert, or_, select, update
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.schema import Column, MetaData, Table
from starlette.requests import Request
from starlette.responses import Response, StreamingResponse
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_304_NOT_MODIFIED,
    HTTP_400_BAD_REQUEST,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_501_NOT_IMPLEMENTED,
)

from ..models.base_interface import Base, BaseInterface, serialize

#
OperatorDict: Final[MappingProxyType[str, operator]] = MappingProxyType(
    {'>=': ge, '<=': le, '>': gt, '<': lt, '!': ne, '=': eq}
)
SQLAlhemyMethodDict: Final[
    MappingProxyType[str, Type[Any]]
] = MappingProxyType(
    {'GET': select, 'POST': insert, 'PUT': update, 'DELETE': delete}
)

SerializedValue = Union[str, int, float]
ColumnFilter = tuple[SerializedValue, operator]


# TODO Optimize count
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

    def get_columns() -> dict[Column, list[ColumnFilter]]:
        columns: dict[Column, list[ColumnFilter]] = {}
        for column in table.columns:
            if getattr(getattr(column.type, 'impl', None), 'python_type', ''):
                type = column.type.impl.python_type
            elif getattr(column.type, 'python_type', None):
                type = column.type.python_type
            else:
                raise HTTPException(
                    HTTP_500_INTERNAL_SERVER_ERROR,
                    f'Could not infer python type for {column}.',
                )

            columns[column] = []
            for value in query_parameters.get(column.key, ()):
                op: operator = eq
                for op_key, op in OperatorDict.items():
                    if value.startswith(op_key):
                        value = value.removeprefix(op_key)
                    elif value.endswith(op_key):
                        value = value.removesuffix(op_key)
                    else:
                        continue
                    break

                if issubclass(type, (int, float)):
                    try:
                        value = type(value)
                    except ValueError as _:
                        raise HTTPException(
                            HTTP_400_BAD_REQUEST,
                            f'Value of parameter "{parameter}" is '
                            f'invalid: {value}',
                        ) from _

                columns[column].append((value, op))
        return columns

    if request.method == 'DELETE':
        async with Session.begin():
            statement = delete(table)
            if any((columns := get_columns()).values()):
                statement = statement.where(
                    or_(
                        *(
                            op(column, value)
                            for column, values in columns.items()
                            for value, op in values
                        )
                    )
                )
            await Session.execute(statement)
        return Response(None, HTTP_204_NO_CONTENT)

    elif request.method in {'POST', 'PUT'}:
        if not isinstance(body := loads(await request.body()), Iterable):
            raise HTTPException(HTTP_400_BAD_REQUEST, 'Body is invalid.')
        elif not body:
            raise HTTPException(HTTP_304_NOT_MODIFIED, 'Body is empty.')

        def modify_item(
            model: Union[Type[BaseInterface], Table],
            item: Union[dict[str, Any], list[dict[str, Any]]],
            /,
            field_chain: tuple[str, ...] = (),
        ) -> dict[str, Any]:
            column_keys, relationship_keys = get_keys(model)
            if isinstance(item, dict):
                if model not in modify_tables:
                    modify_tables[model] = []
                for field, value in dict(item).items():
                    if field in column_keys:
                        column = column_keys[field]
                        if value is None and (
                            column.default is None
                            and (
                                not column.nullable or not column.autoincrement
                            )
                        ):
                            raise HTTPException(
                                HTTP_400_BAD_REQUEST,
                                'Table "{name}" requires fields: '
                                '{fields}.'.format(
                                    name=model.name
                                    if isinstance(model, Table)
                                    else model.__tablename__,
                                    fields=', '.join(
                                        f'"{column.key}"'
                                        for column in column_keys.values()
                                        if column.default is None
                                        and (
                                            not column.nullable
                                            or not column.autoincrement
                                        )
                                    ),
                                ),
                            )
                        else:
                            continue
                    elif relationship_keys is None:
                        raise HTTPException(
                            HTTP_500_INTERNAL_SERVER_ERROR,
                            f'Mapper for table "{model.name}" is not present.',
                        )
                    elif relationship := relationship_keys.get(field):
                        raise HTTPException(
                            HTTP_501_NOT_IMPLEMENTED,
                            'Relationships modification is not supported.',
                        )
                        # try:
                        #     type = relationship.entity.class_
                        #     modify_item(type, value, (*field_chain, field))
                        # except AttributeError as _:
                        #     raise HTTPException(
                        #         HTTP_500_INTERNAL_SERVER_ERROR,
                        #         'Could not infer type for relationship: '
                        #         f'{relationship}',
                        #     ) from _
                    del item[field]
                modify_tables[model].append(item)

            elif item:
                for index, item in enumerate(item):
                    if not isinstance(item, dict):
                        raise HTTPException(
                            HTTP_400_BAD_REQUEST,
                            f'%s element #{index} should be a dictionary.'
                            % '.'.join((route, *field_chain)),
                        )
                    modify_item(model, item)

        modify_tables: dict[Table, list[dict[str, Any]]] = {}
        modify_item(model or table, body)
        async with Session.begin():
            method = insert if request.method == 'POST' else update
            for table, values in modify_tables.items():
                await Session.execute(method(table, values))
        return Response(None, HTTP_204_NO_CONTENT)

    else:

        def get_field(
            model: Union[Type[BaseInterface], Table],
            field: str,
            /,
            field_chain: tuple[str, ...] = (),
            relationship_chain: tuple[RelationshipProperty, ...] = (),
        ) -> Union[Column, tuple[RelationshipProperty, ...]]:
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
                            type = relationship.entity.class_
                            return get_field(
                                type,
                                '.'.join(relationship_fields),
                                (*field_chain, field),
                                (*relationship_chain, getattr(type, field)),
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
            return (
                (*relationship_chain, getattr(model, field))
                if is_relationship
                else column_keys[field]
            )

        column_fields: list[Column] = []
        relationship_options: list = []
        for field in query_parameters.get('field', ()):
            field = get_field(model or table, field)
            if isinstance(field, Column):
                column_fields.append(field)
            elif isinstance(field, RelationshipProperty):
                relationship_options.append(selectinload(field))
            elif isinstance(field, Iterable):
                relationships_chain = iter(field)
                field = next(relationships_chain)
                option = selectinload(field)

                for relationship in relationships_chain:
                    option = option.selectinload(relationship)
                relationship_options.append(option)
            else:
                raise HTTPException(
                    HTTP_500_INTERNAL_SERVER_ERROR,
                    f'Unknwon field in table "{table_name}": {field}',
                )

        statement = select(column_fields or model or table)
        if relationship_options:
            statement = statement.options(*relationship_options)

        if any((columns := get_columns()).values()):
            statement = statement.where(
                or_(
                    *(
                        op(column, value)
                        for column, values in columns.items()
                        for value, op in values
                    )
                )
            )

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

        option: str = request.path_params.get('option', '').lower()
        if option == 'count':
            statement = select(count()).select_from(statement)
            return Response(str(await Session.scalar(statement)))

        elif not option or option == 'stream':
            if orderings := [
                column.asc() if parameter.startswith('asc') else column.desc()
                for parameter, values in query_parameters.items()
                if parameter in {'asc', 'ascending', 'desc', 'descending'}
                for value in values
                if (column := table.columns.get(value)) is not None
            ]:
                statement = statement.order_by(*orderings)

            if not option:
                if column_fields or model is None:
                    result = await Session.execute(statement)
                    return response(list(map(list, result.all())))
                return response((await Session.scalars(statement)).all())

            async def serialize_result():
                async for item in await function(statement):
                    yield dumps(item, default=serialize)

            function = (
                Session.stream
                if column_fields or model is None
                else Session.stream_scalars
            )
            return StreamingResponse(serialize_result())

        else:
            return Response(None, HTTP_406_NOT_ACCEPTABLE)