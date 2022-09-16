from datetime import datetime
from typing import Any, Dict, Final, Optional, Tuple, Union
from uuid import UUID

from sqlalchemy.dialects.postgresql import UUID as sa_UUID
from sqlalchemy.sql.schema import Column, SchemaItem
from sqlalchemy.sql.sqltypes import JSON, DateTime, String

from ..base_interface import Base


class AuditLogEntryModel(Base):

    instance_id: Final[Column[Optional[UUID]]] = Column(
        sa_UUID(as_uuid=True),
        index=True,
    )
    id: Final[Column[UUID]] = Column(sa_UUID(as_uuid=True), primary_key=True)
    payload: Final[Column[Optional[dict]]] = Column(JSON)
    created_at: Final[Optional[datetime]] = Column(DateTime(timezone=True))
    ip_address: Final[Column[str]] = Column(
        String(64),
        nullable=False,
        default='',
    )

    __table_args__: Final[Tuple[Union[SchemaItem, Dict[str, Any]]]] = (
        dict(
            schema='auth',
            comment='Auth: Audit trail for user actions.',
        ),
    )
