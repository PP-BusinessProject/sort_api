from datetime import datetime
from typing import Any, Dict, Final, Optional, Tuple, Union
from uuid import UUID

from sqlalchemy.dialects.postgresql import UUID as sa_UUID
from sqlalchemy.sql.schema import Column, SchemaItem
from sqlalchemy.sql.sqltypes import DateTime, String

from ..base_interface import Base


class InstanceModel(Base):

    id: Final[Column[UUID]] = Column(sa_UUID(as_uuid=True), primary_key=True)
    uuid: Final[Column[Optional[UUID]]] = Column(sa_UUID(as_uuid=True))
    raw_base_config: Final[Column[Optional[str]]] = Column(String)
    user_id: Final[Column[UUID]] = Column(
        sa_UUID(as_uuid=True), nullable=False
    )
    created_at: Final[Optional[datetime]] = Column(DateTime(timezone=True))
    updated_at: Final[Optional[datetime]] = Column(DateTime(timezone=True))

    __table_args__: Final[Tuple[Union[SchemaItem, Dict[str, Any]]]] = (
        dict(
            schema='auth',
            comment='Auth: Manages users across multiple sites.',
        ),
    )
