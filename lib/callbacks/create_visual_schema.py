from logging import Logger
from pathlib import Path
from typing import Any, Final, Optional, Union

from sqlalchemy.sql.schema import MetaData

#
logger: Final[Logger] = Logger(__file__)


def create_visual_schema(
    metadata: MetaData,
    /,
    path: Optional[Union[str, Path]] = None,
    *,
    force: bool = True,
    **kwargs: Any,
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
        from eralchemy2 import render_er
    except ImportError:
        return logger.warning(
            'Cannot proceed visual schema creation. '
            'ERAlchemy is not installed or loaded properly.'
        )

    if force and _exists:
        logger.debug(f'Visual schema deletion at {path.absolute()}')
        path.unlink(missing_ok=True)
    logger.info(f'Visual schema creation at {path.absolute()}')
    render_er(metadata, str(path.absolute()), **kwargs)
