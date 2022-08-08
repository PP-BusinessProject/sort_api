from ast import operator
from asyncio import sleep
from contextlib import suppress
from datetime import date, datetime, time, timedelta
from operator import eq, ge, gt, le, lt, ne
from queue import Empty, Queue
from types import MappingProxyType
from typing import (
    Any,
    AsyncGenerator,
    Dict,
    Final,
    Iterable,
    List,
    Optional,
    Type,
    Union,
)

from dateutil.parser import isoparse
from dateutil.tz.tz import tzlocal
from fastapi.applications import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse
from orjson import dumps, loads
from sqlalchemy.event.api import listen, remove
from sqlalchemy.ext.asyncio.scoping import async_scoped_session
from sqlalchemy.orm import UOWTransaction, selectinload
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import delete, insert, or_, select, update
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.schema import Column, MetaData, Table
from sse_starlette import EventSourceResponse
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_304_NOT_MODIFIED,
    HTTP_400_BAD_REQUEST,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from ..middleware.async_sqlalchemy_middleware import ColumnFilter
from ..models.base_interface import Base, BaseInterface, serialize

#
OperatorDict: Final[MappingProxyType[str, operator]] = MappingProxyType(
    {'>=': ge, '<=': le, '>': gt, '<': lt, '!': ne, '=': eq}
)
InverseOperatorDict: Final[MappingProxyType[operator, str]] = MappingProxyType(
    {ge: '>=', le: '<=', gt: '>', lt: '<', ne: '!', eq: '='}
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

    def get_columns() -> Dict[str, List[ColumnFilter]]:
        columns: Dict[str, List[ColumnFilter]] = {}
        for column in table.columns:
            if getattr(getattr(column.type, 'impl', None), 'python_type', ''):
                type = column.type.impl.python_type
            elif getattr(column.type, 'python_type', None):
                type = column.type.python_type
            else:
                raise HTTPException(
                    HTTP_500_INTERNAL_SERVER_ERROR,
                    f'Could not infer python type for {column.key}.',
                )

            columns[column.key] = []
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

                columns[column.key].append((value, op))
        return columns

    option: str = request.path_params.get('option', '').lower()
    if request.method == 'DELETE':
        async with Session.begin():
            statement = delete(table)
            if option == 'return':
                statement = statement.returning(*table.columns)
            if any((columns := get_columns()).values()):
                statement = statement.where(
                    or_(
                        *(
                            op(getattr(table.c, key), value)
                            for key, values in columns.items()
                            for value, op in values
                        )
                    )
                )
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
                for field, value in dict(item).items():
                    if field in column_keys:
                        if field in {'created_at', 'updated_at'}:
                            del item[field]
                            continue
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

                        type = None
                        with suppress(NotImplementedError):
                            type = column.type.python_type
                        if type is None or isinstance(value, type):
                            pass
                        elif type == date:
                            item[field] = isoparse(value).date()
                        elif type == time:
                            item[field] = isoparse(value).time()
                        elif type == datetime:
                            item[field] = isoparse(value)
                        elif type == timedelta:
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
                map(items, Session.add)
            else:
                items = [await Session.merge(item) for item in items]

        if option == 'return':
            return response(items)
        else:
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
                option_ = selectinload(field)

                for relationship in relationships_chain:
                    option_ = option_.selectinload(relationship)
                relationship_options.append(option_)
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
                        op(getattr(table.c, key), value)
                        for key, values in columns.items()
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

            if isinstance(session := Session.session_factory, sessionmaker):
                session = session.class_
            session = getattr(session, 'sync_session_class', session)

            async def serialize_result() -> AsyncGenerator[bytes, None]:
                nonlocal request, queue, _after_flush
                try:
                    while not await request.is_disconnected():
                        while True:
                            try:
                                prev, items = queue.get(timeout=1)
                                if not prev or not items:
                                    continue
                                payload = dict(
                                    prev_value=prev,
                                    value=items,
                                    timestamp=datetime.now(tzlocal()),
                                )
                                yield dumps(payload, default=serialize)
                            except Empty:
                                await sleep(1)
                                break
                finally:
                    remove(session, 'after_flush', _after_flush)

            def _after_flush(_: Any, context: UOWTransaction, /) -> None:
                nonlocal queue, columns
                if states := [
                    state
                    for state in context.states
                    if table in state.mapper.tables
                    and all(
                        operator(getattr(state.attrs, column).value, value)
                        for column, operators in columns.items()
                        for value, operator in operators
                    )
                ]:
                    prev_items = [
                        state.class_.from_previous_state(state)
                        if state.persistent
                        else state.object
                        for state in states
                        if context.is_deleted(state) or state.persistent
                    ]
                    items = [
                        state.object
                        for state in states
                        if not context.is_deleted(state)
                    ]
                    queue.put((prev_items, items))

            queue = Queue()
            listen(session, 'after_flush', _after_flush)
            return EventSourceResponse(
                serialize_result(),
                ping=5,
                ping_message_factory=lambda: dumps(
                    dict(
                        prev_value=[],
                        value=[],
                        timestamp=datetime.now(tzlocal()),
                    ),
                    default=serialize,
                ),
            )
        else:
            return Response(None, HTTP_406_NOT_ACCEPTABLE)
