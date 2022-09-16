from datetime import datetime
from typing import Any, Dict, Final, Optional, Tuple, Union
from uuid import UUID

from sqlalchemy.dialects.postgresql import UUID as sa_UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey, Index, SchemaItem
from sqlalchemy.sql.sqltypes import BigInteger, Boolean, DateTime, String
from typing_extensions import Self

from ..base_interface import Base
from .session_model import SessionModel


class RefreshTokenModel(Base):

    instance_id: Final[Column[Optional[UUID]]] = Column(
        sa_UUID(as_uuid=True),
        index=True,
    )
    id: Final[Column[int]] = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    token: Final[Column[Optional[str]]] = Column(String(255), unique=True)
    user_id: Final[Column[Optional[str]]] = Column(String(255))
    revoked: Final[Column[Optional[bool]]] = Column(Boolean)
    created_at: Final[Optional[datetime]] = Column(DateTime(timezone=True))
    updated_at: Final[Optional[datetime]] = Column(DateTime(timezone=True))
    parent: Final[Column[Optional[str]]] = Column(
        token.type,
        ForeignKey(token, onupdate='NO ACTION', ondelete='NO ACTION'),
        index=True,
    )
    session_id: Final[Column[UUID]] = Column(
        SessionModel.id.type,
        ForeignKey(SessionModel.id, onupdate='NO ACTION', ondelete='CASCADE'),
    )

    session: Final['RelationshipProperty[SessionModel]'] = relationship(
        'SessionModel',
        back_populates='refresh_tokens',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    parent_: Final['RelationshipProperty[Optional[Self]]'] = relationship(
        'RefreshTokenModel',
        back_populates='children',
        lazy='noload',
        cascade='save-update',
        remote_side=[token],
        uselist=False,
    )
    children: Final['RelationshipProperty[list[Self]]'] = relationship(
        'RefreshTokenModel',
        back_populates='parent_',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )

    __table_args__: Final[Tuple[Union[SchemaItem, Dict[str, Any]]]] = (
        Index(None, token),
        Index(
            'ix_auth_refresh_tokens_instance_id_user_id', instance_id, user_id
        ),
        dict(
            schema='auth',
            comment='Auth: Store of tokens used to refresh JWT tokens once '
            'they expire.',
        ),
    )
