from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Final, Optional, Tuple, Union
from uuid import UUID

from sqlalchemy.dialects.postgresql import UUID as sa_UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey, SchemaItem
from sqlalchemy.sql.sqltypes import DateTime

from ..base_interface import Base
from .user_model import UserModel

if TYPE_CHECKING:
    from .refresh_token_model import RefreshTokenModel


class SessionModel(Base):

    id: Final[Column[UUID]] = Column(
        UserModel.id.type,
        ForeignKey(UserModel.id, onupdate='NO ACTION', ondelete='CASCADE'),
        primary_key=True,
    )
    user_id: Final[Column[UUID]] = Column(
        sa_UUID(as_uuid=True), nullable=False
    )
    created_at: Final[Optional[datetime]] = Column(DateTime(timezone=True))
    updated_at: Final[Optional[datetime]] = Column(DateTime(timezone=True))

    user: Final['RelationshipProperty[UserModel]'] = relationship(
        'UserModel',
        back_populates='sessions',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    refresh_tokens: Final[
        'RelationshipProperty[list[RefreshTokenModel]]'
    ] = relationship(
        'RefreshTokenModel',
        back_populates='session',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )

    __table_args__: Final[Tuple[Union[SchemaItem, Dict[str, Any]]]] = (
        dict(
            schema='auth',
            comment='Auth: Stores session data associated to a user.',
        ),
    )
