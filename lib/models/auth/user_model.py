from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, Final, Optional, Tuple, Union
from uuid import UUID

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as sa_UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.expression import and_, literal_column
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import (
    CheckConstraint,
    Column,
    Computed,
    Index,
    SchemaItem,
)
from sqlalchemy.sql.sqltypes import Boolean, DateTime, SmallInteger, String

from ..base_interface import Base

if TYPE_CHECKING:
    from ..companies.company_model import CompanyModel
    from ..people.person_model import PersonModel
    from .identity_model import IdentityModel
    from .session_model import SessionModel


class UserModel(Base):
    instance_id: Final[Column[Optional[UUID]]] = Column(sa_UUID(as_uuid=True))
    id: Final[Column[UUID]] = Column(
        sa_UUID(as_uuid=True), primary_key=True, default=lambda: UUID()
    )
    aud: Final[Column[Optional[str]]] = Column(String(255))
    role: Final[Column[Optional[str]]] = Column(String(255))
    email: Final[Column[Optional[str]]] = Column(String(255), unique=True)
    encrypted_password: Final[Column[Optional[str]]] = Column(String(255))
    email_confirmed_at: Final[Optional[datetime]] = Column(
        DateTime(timezone=True)
    )
    invited_at: Final[Optional[datetime]] = Column(DateTime(timezone=True))
    confirmation_token: Final[Column[Optional[str]]] = Column(String(255))
    confirmation_sent_at: Final[Optional[datetime]] = Column(
        DateTime(timezone=True)
    )
    recovery_token: Final[Column[Optional[str]]] = Column(String(255))
    recovery_sent_at: Final[Optional[datetime]] = Column(
        DateTime(timezone=True)
    )
    email_change_token_new: Final[Column[Optional[str]]] = Column(String(255))
    email_change: Final[Column[Optional[str]]] = Column(String(255))
    email_change_sent_at: Final[Optional[datetime]] = Column(
        DateTime(timezone=True)
    )
    last_sign_in_at: Final[Optional[datetime]] = Column(
        DateTime(timezone=True)
    )
    raw_app_meta_data: Final[Optional[dict]] = Column(JSONB)
    raw_user_meta_data: Final[Optional[dict]] = Column(JSONB)
    is_super_admin: Final[Optional[bool]] = Column(Boolean)
    created_at: Final[Optional[datetime]] = Column(DateTime(timezone=True))
    updated_at: Final[Optional[datetime]] = Column(DateTime(timezone=True))
    phone: Final[Column[Optional[str]]] = Column(
        String(15), default=None, unique=True
    )
    phone_confirmed_at: Final[Optional[datetime]] = Column(
        DateTime(timezone=True)
    )
    phone_change: Final[Column[Optional[str]]] = Column(String(15), default='')
    phone_change_token: Final[Column[Optional[str]]] = Column(
        String(255), default=''
    )
    phone_change_sent_at: Final[Optional[datetime]] = Column(
        DateTime(timezone=True)
    )
    confirmed_at: Final[Optional[datetime]] = Column(
        DateTime(timezone=True),
        Computed('LEAST(email_confirmed_at, phone_confirmed_at)'),
    )
    email_change_token_current: Final[Column[Optional[str]]] = Column(
        String(255), default=''
    )
    email_change_confirm_status: Final[Column[Optional[int]]] = Column(
        SmallInteger,
        CheckConstraint(
            and_(
                literal_column('email_change_confirm_status')
                >= literal_column('0'),
                literal_column('email_change_confirm_status')
                <= literal_column('2'),
            )
        ),
        default=0,
    )
    banned_until: Final[Optional[datetime]] = Column(DateTime(timezone=True))
    reauthentication_token: Final[Column[Optional[str]]] = Column(
        String(255), default=''
    )
    reauthentication_sent_at: Final[Optional[datetime]] = Column(
        DateTime(timezone=True)
    )

    identities: Final[
        'RelationshipProperty[list[IdentityModel]]'
    ] = relationship(
        'IdentityModel',
        back_populates='user',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    sessions: Final['RelationshipProperty[list[SessionModel]]'] = relationship(
        'SessionModel',
        back_populates='user',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )

    company: Final[
        'RelationshipProperty[Optional[CompanyModel]]'
    ] = relationship(
        'CompanyModel',
        back_populates='user',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    person: Final[
        'RelationshipProperty[Optional[PersonModel]]'
    ] = relationship(
        'PersonModel',
        back_populates='user',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )

    __table_args__: Final[Tuple[Union[SchemaItem, Dict[str, Any]]]] = (
        Index(
            None,
            confirmation_token,
            unique=True,
            postgresql_where=confirmation_token.op('!~')('^[0-9 ]*$'),
        ),
        Index(
            None,
            email_change_token_current,
            unique=True,
            postgresql_where=email_change_token_current.op('!~')('^[0-9 ]*$'),
        ),
        Index(
            None,
            email_change_token_new,
            unique=True,
            postgresql_where=email_change_token_new.op('!~')('^[0-9 ]*$'),
        ),
        Index(
            None,
            reauthentication_token,
            unique=True,
            postgresql_where=reauthentication_token.op('!~')('^[0-9 ]*$'),
        ),
        Index(
            None,
            recovery_token,
            unique=True,
            postgresql_where=recovery_token.op('!~')('^[0-9 ]*$'),
        ),
        Index(
            'ix_auth_users_instance_id_email', instance_id, func.lower(email)
        ),
        Index(None, instance_id),
        dict(
            schema='auth',
            comment='Auth: Stores user login data within a secure schema.',
        ),
    )
