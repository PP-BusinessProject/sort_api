from logging import Logger
from pathlib import Path
from typing import Final, Optional, Union

from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.inspection import inspect
from sqlalchemy.sql.schema import MetaData

#
logger: Final[Logger] = Logger(__file__)


async def create_visual_schema(
    metadata: MetaData,
    /,
    path: Optional[Union[str, Path]] = None,
    *,
    force: bool = False,
) -> None:
    if not isinstance(metadata, MetaData):
        raise ValueError(f'MetaData is of the wrong type "{type(metadata)}".')
    if isinstance(path, str):
        path = Path(path).resolve()
    if not isinstance(path, Path):
        path = Path('./schema.png').resolve()

    if (_exists := path.exists()) and not force:
        return logger.debug(
            'Visual schema creation skipped. '
            f'Visual schema alredy exists at {path.absolute()}'
        )

    try:
        from eralchemy2.main import (
            all_to_intermediary,
            filter_resources,
            get_output_mode,
        )
    except ImportError:
        return logger.warning(
            'Cannot proceed visual schema creation. '
            'ERAlchemy is not installed or loaded properly.'
        )

    if force and _exists:
        logger.debug(f'Visual schema deletion at {path.absolute()}')
        path.unlink(missing_ok=True)
    logger.info(f'Visual schema creation at {path.absolute()}')

    def process_data(connection):
        tables, relationships = all_to_intermediary(metadata)
        _tables = {}
        inspector = inspect(connection)
        for schema in inspector.get_schema_names():
            for table in inspector.get_table_names(schema):
                _tables[table] = schema

        for relationship in relationships:
            if relationship.left_col in _tables:
                schema = _tables[relationship.left_col]
                if schema != 'public':
                    relationship.left_col = f'{schema}.{relationship.left_col}'
            if relationship.right_col in _tables:
                schema = _tables[relationship.right_col]
                if schema != 'public':
                    relationship.right_col = (
                        f'{schema}.{relationship.right_col}'
                    )
        tables, relationships = filter_resources(tables, relationships)
        intermediary_to_output = get_output_mode(str(path.absolute()), 'auto')
        intermediary_to_output(tables, relationships, str(path.absolute()))

    if isinstance(metadata.bind, AsyncEngine):
        async with metadata.bind.begin() as conn:
            await conn.run_sync(process_data)
    else:
        process_data(metadata.bind)
