from asyncio import WindowsSelectorEventLoopPolicy, run, set_event_loop_policy
from contextlib import suppress
from decimal import Decimal
from enum import Enum, Flag
from logging import basicConfig
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Optional, Type

from orjson import dumps
from sqlalchemy.orm.mapper import Mapper
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column


async def main(
    declarative_base: 'Type[_DeclarativeBase]',
    /,
    export_path: Path = Path('./export.json').resolve(),
    *,
    remove_duplicate_paths: bool = True,
    single_path: Optional[Path] = None,
) -> None:
    registry: dict[str, Mapper] = {
        class_.__mapper__._sort_key: class_.__mapper__
        for name, class_ in (
            declarative_base._sa_registry._class_registry.items()
        )
        if not name.startswith('_')
    }

    if single_path is not None:
        registry = {
            '.'.join((*single_path.parts, k.split('.')[-1])): v
            for k, v in registry.items()
        }

    elif remove_duplicate_paths:
        duplicate_parts: Optional[list[str]] = None
        for name, mapper in registry.items():
            if name.startswith('_'):
                continue
            elif duplicate_parts is None:
                duplicate_parts = mapper._sort_key.split('.')
                continue

            parts: list[str] = mapper._sort_key.split('.')
            if len(duplicate_parts) < len(parts):
                duplicate_parts += [None] * (len(parts) - len(duplicate_parts))
            elif len(parts) < len(duplicate_parts):
                parts += [None] * (len(duplicate_parts) - len(parts))

            for index, (value1, value2) in enumerate(
                zip(duplicate_parts, parts)
            ):
                if value1 != value2:
                    duplicate_parts = duplicate_parts[:index]
                    break
        if duplicate_path := '.'.join(duplicate_parts) + '.':
            registry = {
                k.removeprefix(duplicate_path): v for k, v in registry.items()
            }

    tables: dict[str, dict[str, dict[str, Any]]] = {}
    for key, mapper in registry.items():
        tables[key] = {}
        column: Column
        for column in mapper.columns:
            default = None
            if column.default is not None:
                if isinstance(arg := column.default.arg, Enum):
                    default = str(arg).removeprefix(
                        f'{arg.__class__.__name__}.'
                    )
                elif not isinstance(column.default.arg, Callable):
                    with suppress(TypeError):
                        default = serialize(column.default.arg)
                        if isinstance(default, Decimal):
                            default = float(default)

            type, iterable = str, False
            with suppress(NotImplementedError):
                type = column.type.python_type
            if issubclass(type, Decimal):
                type = float
            if issubclass(type, list):
                type, iterable = column.type.item_type.type.python_type, True
            tables[key][column.key] = dict(
                type=f"%s[{', '.join(type._member_map_)}]"
                % ('flag' if issubclass(type, Flag) else 'enum')
                if issubclass(type, Enum)
                else f'{type.__name__.lower()}[]'
                if iterable
                else type.__name__.lower(),
                default=default,
                doc=column.doc,
                nullable=bool(
                    column.autoincrement is True
                    or column.foreign_keys
                    or (column.default is not None and default is None)
                    or column.nullable
                ),
                compare=type in (int, float, str)
                and column in mapper.primary_key,
                equality=column.key not in {'created_at', 'updated_at'},
            )

        relationship: RelationshipProperty
        for relationship in mapper.relationships:
            for _key, mapper in registry.items():
                if mapper._sort_key == relationship.entity._sort_key:
                    break
            else:
                raise
            tables[key][relationship.key] = dict(
                type=f'{_key}[]' if relationship.uselist else _key,
                default=[] if relationship.uselist else None,
                doc=relationship.doc,
                nullable=not relationship.uselist,
                equality=False,
            )

    with open(export_path, 'wb') as export:
        export.write(dumps(tables))


if __name__ == '__main__':
    from .models.base_interface import Base, serialize

    if TYPE_CHECKING:
        from .models.base_interface import _DeclarativeBase

    basicConfig(level='DEBUG')
    set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    run(main(Base, single_path=Path()))
