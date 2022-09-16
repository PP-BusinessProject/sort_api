from typing import TYPE_CHECKING, Final
from uuid import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from ..._mixins import Timestamped
from ...base_interface import Base
from ..company_model import CompanyModel
from .types.company_contact_type_model import CompanyContactTypeModel

if TYPE_CHECKING:
    from .company_contact_locale_model import CompanyContactLocaleModel


class CompanyContactModel(Timestamped, Base):
    company_id: Final[Column[UUID]] = Column(
        CompanyModel.user_id.type,
        ForeignKey(
            CompanyModel.user_id, onupdate='CASCADE', ondelete='CASCADE'
        ),
        nullable=False,
    )
    id: Final[Column[int]] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    type_id: Final[Column[int]] = Column(
        CompanyContactTypeModel.id.type,
        ForeignKey(
            CompanyContactTypeModel.id,
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        nullable=False,
    )

    fallback_first_name: Final[Column[str]] = Column(
        String(64),
        CheckConstraint("fallback_first_name <> ''"),
        nullable=False,
    )
    fallback_last_name: Final[Column[str]] = Column(
        String(64),
        nullable=False,
        default='',
    )

    locales: Final[
        'RelationshipProperty[list[CompanyContactLocaleModel]]'
    ] = relationship(
        'CompanyContactLocaleModel',
        back_populates='contact',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    company: Final['RelationshipProperty[CompanyModel]'] = relationship(
        'CompanyModel',
        back_populates='contacts',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    type: Final[
        'RelationshipProperty[CompanyContactTypeModel]'
    ] = relationship(
        'CompanyContactTypeModel',
        back_populates='contacts',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
