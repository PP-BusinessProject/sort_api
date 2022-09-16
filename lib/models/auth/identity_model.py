from datetime import datetime
from typing import Any, Dict, Final, Optional, Tuple, Union
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.schema import Column, SchemaItem
from sqlalchemy.sql.sqltypes import DateTime, String

from ..base_interface import Base
from .user_model import UserModel
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty


class IdentityModel(Base):

    id: Final[Column[str]] = Column(String, primary_key=True)
    user_id: Final[Column[UUID]] = Column(
        UserModel.id.type,
        ForeignKey(UserModel.id, onupdate='NO ACTION', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    identity_data: Final[Column[dict]] = Column(JSONB, nullable=False)
    provider: Final[Column[str]] = Column(String, primary_key=True)
    last_sign_in_at: Final[Optional[datetime]] = Column(
        DateTime(timezone=True)
    )
    created_at: Final[Optional[datetime]] = Column(DateTime(timezone=True))
    updated_at: Final[Optional[datetime]] = Column(DateTime(timezone=True))

    user: Final['RelationshipProperty[UserModel]'] = relationship(
        'UserModel',
        back_populates='identities',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )

    __table_args__: Final[Tuple[Union[SchemaItem, Dict[str, Any]]]] = (
        dict(
            schema='auth',
            comment='Auth: Stores identities associated to a user.',
        ),
    )
