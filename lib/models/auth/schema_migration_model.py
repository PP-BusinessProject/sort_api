from typing import Any, Dict, Final, Tuple, Union
from uuid import UUID

from sqlalchemy.dialects.postgresql import UUID as sa_UUID
from sqlalchemy.sql.schema import Column, SchemaItem
from sqlalchemy.sql.sqltypes import String

from ..base_interface import Base


class SchemaMigrationModel(Base):

    version: Final[Column[UUID]] = Column(
        String(255),
        primary_key=True,
    )
    user_id: Final[Column[UUID]] = Column(
        sa_UUID(as_uuid=True), nullable=False
    )

    __table_args__: Final[Tuple[Union[SchemaItem, Dict[str, Any]]]] = (
        dict(
            schema='auth',
            comment='Auth: Manages updates to the auth system.',
        ),
    )
