from ast import operator
from contextlib import suppress
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from inspect import isclass
from operator import eq, ge, gt, le, lt, ne
from types import MappingProxyType
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Dict,
    Final,
    Iterable,
    List,
    Optional,
    Tuple,
    Type,
    Union,
)
from urllib.parse import unquote

from dateutil.parser import isoparse
from fastapi.applications import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse
from orjson import loads
from sqlalchemy.ext.asyncio.scoping import async_scoped_session
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.expression import and_, delete, or_, select
from sqlalchemy.sql.functions import count as sa_count
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column, ColumnClause, MetaData, Table
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_304_NOT_MODIFIED,
    HTTP_400_BAD_REQUEST,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from typing_extensions import Self

from ..models.base_interface import BaseInterface


def _get_keys(
    model: Union[Type[BaseInterface], Table],
) -> tuple[dict[str, Column], Optional[dict[str, RelationshipProperty]]]:
    return (
        {_.key: _ for _ in model.columns if _.key},
        {_.key: _ for _ in model.relationships if _.key}
        if isclass(model) and issubclass(model, BaseInterface)
        else None,
    )


async def endpoint(request: Request, /) -> Response:
    return await EndPoint(request)()


@dataclass(init=False, frozen=True)
class EndPoint(object):

    request: Final[Request]
    app: Final[FastAPI]
    Session: Final[async_scoped_session]
    metadata: Final[MetaData]

    if TYPE_CHECKING:
        from sqlalchemy.orm.decl_api import _DeclarativeBase

        Base: Final[Type[_DeclarativeBase]]

    _tables_registry: ClassVar[Dict[str, Union[Table, BaseInterface]]] = {}

    def __init__(self: Self, request: Request, /) -> None:
        if not isinstance(app := request.get('app'), FastAPI):
            raise HTTPException(
                HTTP_500_INTERNAL_SERVER_ERROR, 'App is not present.'
            )
        if not isinstance(
            Session := request.get('Session'), async_scoped_session
        ):
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
        object.__setattr__(self, 'request', request)
        object.__setattr__(self, 'app', app)
        object.__setattr__(self, 'Session', Session)
        object.__setattr__(self, 'metadata', metadata)
        object.__setattr__(self, 'Base', request.get('Base'))

    async def __call__(self: Self, /) -> Response:
        route: Final[str] = self.request.path_params.get('route', '').lower()
        if not route or (model := self._get_model(route)) is None:
            raise HTTPException(
                HTTP_400_BAD_REQUEST, 'Route is not determined.'
            )

        if self.request.method == 'DELETE':
            async with self.Session.begin():
                statement = (
                    EndPointStatementBuilder.delete(model, query)
                    if (query := self.request.url.query)
                    else delete(model)
                )
                await self.Session.execute(statement)
            return Response(None, HTTP_204_NO_CONTENT)

        elif self.request.method in {'POST', 'PUT'}:
            try:
                body = loads(await self.request.body())
                if not isinstance(body, Iterable):
                    raise ValueError
                elif isinstance(body, list) and not body:
                    raise HTTPException(
                        HTTP_304_NOT_MODIFIED, 'Body is empty.'
                    )
            except ValueError as _:
                raise HTTPException(
                    HTTP_400_BAD_REQUEST, 'Body is invalid.'
                ) from _

            items = []
            if isinstance(body, dict):
                items.append(self._modify_item(model, body))
            elif isinstance(body, Iterable):
                items.extend(self._modify_item(model, item) for item in body)
            async with self.Session.begin():
                if self.request.method == 'POST':
                    for item in items:
                        self.Session.add(item)
                else:
                    for item in items:
                        await self.Session.merge(item)
            return Response(None, HTTP_204_NO_CONTENT)

        else:
            limit: int = 0
            offset: int = 0
            count: bool = False
            option1: str = self.request.path_params.get('option1', None)
            if option1 is not None:
                if option1.isdecimal():
                    limit = int(option1)
                elif option1.lower() == 'count':
                    count = True
                elif option1:
                    raise HTTPException(
                        HTTP_400_BAD_REQUEST, 'Limit is invalid.'
                    )

                option2: str = self.request.path_params.get('option2', None)
                if option2 is not None:
                    if option2.isdecimal():
                        offset = int(option2)
                    elif option2.lower() == 'count':
                        count = True
                    elif option2:
                        raise HTTPException(
                            HTTP_400_BAD_REQUEST, 'Offset is invalid.'
                        )

                    option3: str = self.request.path_params.get('option3', '')
                    if option3.lower() == 'count':
                        count = True

            statement, is_raw = (
                EndPointStatementBuilder.select(
                    model, query, limit=limit, offset=offset, count=count
                )
                if (query := self.request.url.query)
                else (select(model), isinstance(model, Table))
            )
            if count:
                return Response(str(await self.Session.scalar(statement) or 0))

            try:
                response = self._get_response_class()
                if is_raw:
                    result = await self.Session.execute(statement)
                    return response(list(map(list, result.all())))
                return response((await self.Session.scalars(statement)).all())
            except TypeError as _:
                raise HTTPException(
                    HTTP_500_INTERNAL_SERVER_ERROR,
                    'Request was valid, but response could not be processed '
                    'correctly.',
                ) from _

    def _get_response_class(self: Self, /) -> Type[Response]:
        return (
            getattr(self.app.router, 'default_response_class', None)
            or ORJSONResponse
        )

    def _get_model_name(self: Self, route: str, /) -> Optional[str]:
        if isinstance(table := self._get_model(route), BaseInterface):
            table = table.__table__
        return table.name if isinstance(table, Table) else None

    def _get_model(
        self: Self,
        route: str,
        /,
    ) -> Union[None, Table, BaseInterface]:
        if route not in self.__class__._tables_registry:
            registry = self.Base.registry if self.Base is not None else None
            for table_name, table in self.metadata.tables.items():
                if route == table_name.lower():
                    if registry is not None:
                        for decl in registry._class_registry.data.values():
                            if decl.key.startswith('_'):
                                pass
                            elif (model := decl()).__tablename__ == table_name:
                                self.__class__._tables_registry[route] = model
                                break
                        else:
                            self.__class__._tables_registry[route] = table
                        break
                    self.__class__._tables_registry[route] = table
                    break
            else:
                return None
        return self.__class__._tables_registry[route]

    def _modify_item(
        self: Self,
        model: Union[Type[BaseInterface], Table],
        item: Union[dict[str, Any], list[dict[str, Any]]],
        /,
        field_chain: tuple[str, ...] = (),
    ) -> dict[str, Any]:
        column_keys, relationship_keys = _get_keys(model)
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
                    if ctype is None or isinstance(value, (ctype, type(None))):
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
                        f"Mapper for table '{model.name}' is not present.",
                    )
                elif relationship := relationship_keys.get(field):
                    if not value:
                        del item[field]
                        continue
                    try:
                        item[field] = self.modify_item(
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
                        % ('.'.join(field_chain) or 'Root'),
                    )
                items.append(self.modify_item(model, item, field_chain))
            return items


@dataclass(init=False, frozen=True)
class EndPointStatementBuilder(object):
    Key = Tuple[
        Iterable[RelationshipProperty],
        Union[Column, InstrumentedAttribute],
    ]
    SerializedValue = Union[str, int, float]
    ColumnFilter = Tuple[SerializedValue, Union[str, operator]]

    OperatorDict: Final[
        MappingProxyType[str, Optional[operator]]
    ] = MappingProxyType(
        {'@@': None, '@>': None}
        | {'>=': ge, '<=': le, '>': gt, '<': lt, '!=': ne, '=': eq}
    )

    @classmethod
    def select(
        cls: Type[Self],
        model: Union[Type[BaseInterface], Table],
        /,
        query: str,
        *,
        limit: int = 0,
        offset: int = 0,
        count: bool = False,
    ) -> Tuple[ColumnClause, bool]:
        registry, filters = cls._process(model, query)
        fields: list[InstrumentedAttribute] = []
        join_options: set[RelationshipProperty] = set()
        load_options: list[selectinload] = []
        orderings: list[ColumnClause] = []
        if not count:
            for _orderings in registry.values():
                orderings.extend(_orderings)

        or_clauses: list[ColumnClause] = []
        for group_filters in filters:
            and_clauses: list[ColumnClause] = []
            for (chain, field), (value, op) in group_filters:
                if isinstance(field, Column):
                    for link in chain:
                        if link not in join_options:
                            join_options.add(link)
                if isinstance(op, str):
                    if op == '@@':
                        clause = field.op(op)(func.to_tsquery(value))
                    else:
                        clause = field.op(op)(value)
                elif op is not None:
                    clause = op(field, value)
                else:
                    fields.append(
                        field if isinstance(field, Column) else (*chain, field)
                    )
                    continue
                and_clauses.append(clause)
            if and_clauses:
                or_clauses.append(and_(*and_clauses))

        raw_select = any(isinstance(field, Column) for field in fields)
        if not count:
            for field in fields:
                if not isinstance(field, Column):
                    if raw_select:
                        for link in field:
                            if link not in join_options:
                                join_options.add(link)
                    else:
                        option = selectinload(next(chain := iter(field)))
                        for link in chain:
                            option = option.selectinload(link)
                        load_options.append(option)

        if raw_select:
            result = [
                _ if isinstance(_, Column) else _[-1].property.entity.class_
                for _ in fields
            ]
        elif count and not limit and not offset:
            result = sa_count()
        else:
            result = model

        statement = select(result)
        for link in join_options:
            statement = statement.join(link)
        if or_clauses:
            statement = statement.where(or_(*or_clauses))
        if orderings:
            statement = statement.order_by(*orderings)
        if load_options:
            statement = statement.options(*load_options)
        if limit:
            statement = statement.limit(limit)
        if offset:
            statement = statement.offset(offset)
        if count and (raw_select or limit or offset):
            statement = select(sa_count()).select_from(statement)
        return statement, raw_select or isinstance(model, Table)

    @classmethod
    def delete(
        cls: Type[Self],
        model: Union[Type[BaseInterface], Table],
        /,
        query: str,
    ) -> ColumnClause:
        registry, filters = cls._process(model, query)
        or_clauses: list[ColumnClause] = []
        for group_filters in filters:
            and_clauses: list[ColumnClause] = []
            for (chain, field), (value, op) in group_filters:
                if isinstance(op, str):
                    if op == '@@':
                        clause = field.op(op)(func.to_tsquery(value))
                    else:
                        clause = field.op(op)(value)
                elif op is not None:
                    clause = op(field, value)
                else:
                    continue
                and_clauses.append(clause)
            if and_clauses:
                or_clauses.append(and_(*and_clauses))

        statement = delete(model)
        if or_clauses:
            statement = statement.where(or_(*or_clauses))
        return statement

    @classmethod
    def _process(
        cls: Type[Self],
        model: Union[Type[BaseInterface], Table],
        query: str,
        /,
    ) -> Tuple[
        Dict[Key, Iterable[ColumnClause]], List[List[Tuple[Key, ColumnFilter]]]
    ]:
        registry, filters = {}, []
        for entity_group in unquote(query.replace('+', ' ')).split('|'):
            group_filters: List = []
            for entity in entity_group.split('&'):
                (name, value), (op_key, op) = cls._process_query(entity)
                *chain, field = cls._get_field(model, name)
                field_property = getattr(field, 'property', field)
                field = getattr(field_property, 'expression', field)
                if (key := (tuple(chain), field)) not in registry:
                    registry[key] = []
                if not isinstance(field, Column):
                    group_filters.append((key, (value, op or op_key)))
                    continue

                if name.endswith('..'):
                    registry[key].append(field.desc())
                elif name.endswith('.'):
                    registry[key].append(field.asc())

                try:
                    value = cls._get_column_value(field, value)
                    group_filters.append((key, (value, op or op_key)))
                except ValueError as e:
                    column_type = cls._get_column_type(field)
                    raise HTTPException(
                        HTTP_400_BAD_REQUEST,
                        f"Value of type '{type(value).__name__}' of "
                        f"parameter '{name}' is invalid, should be valid "
                        f"value of type '{column_type.__name__}'.",
                    ) from e
            if group_filters:
                filters.append(group_filters)
        return registry, filters

    @classmethod
    def _process_query(
        cls: Type[Self],
        entity: str,
        /,
    ) -> Tuple[
        Tuple[str, Optional[str]], Tuple[Optional[str], Optional[operator]]
    ]:
        for op_key, op in cls.OperatorDict.items():
            for _ in ('=', ''):
                name, separator, value = entity.partition(_ + op_key)
                if separator:
                    return (name, value), (op_key, op)
        return (entity, None), (None, None)

    @staticmethod
    def _get_column_type(column: Column) -> Optional[Type]:
        if getattr(getattr(column.type, 'impl', None), 'python_type', ''):
            return column.type.impl.python_type
        elif getattr(column.type, 'python_type', None):
            return column.type.python_type
        return None

    @classmethod
    def _get_column_value(
        cls: Type[Self],
        column: Column,
        value: str,
        /,
    ) -> Optional[Any]:
        if (column_type := cls._get_column_type(column)) is None:
            raise HTTPException(
                HTTP_500_INTERNAL_SERVER_ERROR,
                f'Could not infer python type for {column.key}.',
            )

        if value is not None:
            value = unquote(value.replace('+', ' '))
        if not value and not issubclass(column_type, str):
            if not column.nullable:
                return None
            value = None
        elif issubclass(column_type, bool):
            if value not in {'true', 'false', '1', '0'}:
                raise ValueError
            value = value in {'true', '1'}
        elif issubclass(column_type, (int, float, Decimal)):
            value = column_type(value)
        elif issubclass(column_type, timedelta):
            value = timedelta(seconds=float(value))
        elif issubclass(column_type, date):
            value = isoparse(value).date()
        elif issubclass(column_type, time):
            value = isoparse(value).time()
        elif issubclass(column_type, datetime):
            value = isoparse(value)
        return value

    @classmethod
    def _get_field(
        cls: Type[Self],
        model: Union[Type[BaseInterface], Table],
        field: str,
        /,
        chain: tuple[RelationshipProperty, ...] = (),
    ) -> Tuple[
        Tuple[RelationshipProperty, ...], Union[Column, InstrumentedAttribute]
    ]:
        if not isinstance(table := model, Table):
            table = model.__table__
        column_keys, relationship_keys = _get_keys(model)
        field, *relationship_fields = field.split('.')
        if is_relationship := field not in column_keys:
            if relationship_keys is None:
                raise HTTPException(
                    HTTP_500_INTERNAL_SERVER_ERROR,
                    f"Mapper for table '{table.name}' is not present.",
                )
            if field not in relationship_keys:
                table_or_relationship = 'relationship' if chain else 'table'
                raise HTTPException(
                    HTTP_400_BAD_REQUEST,
                    f"Field '{field}' is not present in the '%s' "
                    f'{table_or_relationship}. '
                    % '.'.join((table.name, *(_.key for _ in chain)))
                    + 'Available fields: %s.'
                    % ', '.join(
                        f"'{_}'" for _ in (*column_keys, *relationship_keys)
                    ),
                )

        if is_relationship and any(relationship_fields):
            for relationship in relationship_keys.values():
                if relationship.key == field:
                    try:
                        return cls._get_field(
                            relationship.entity.class_,
                            '.'.join(relationship_fields),
                            (*chain, getattr(model, field)),
                        )
                    except AttributeError as _:
                        raise HTTPException(
                            HTTP_500_INTERNAL_SERVER_ERROR,
                            'Could not infer type for relationship: '
                            f'{relationship}',
                        ) from _

            raise HTTPException(
                HTTP_400_BAD_REQUEST,
                f"Relationship '{field}' is not present in %s."
                % '.'.join((table.name, *(_.key for _ in chain))),
            )
        return *chain, getattr(
            getattr(model, 'columns', model)
            if isinstance(model, Table)
            else model,
            field,
        )
