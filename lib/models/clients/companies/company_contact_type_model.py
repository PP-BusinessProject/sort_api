from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, CheckConstraint
from sqlalchemy.sql.sqltypes import Integer, String

from ..._mixins import Timestamped
from ...base_interface import Base

if TYPE_CHECKING:
    from .company_contact_model import CompanyContactModel
    from .company_contact_type_locale_model import (
        CompanyContactTypeLocaleModel,
    )


class CompanyContactTypeModel(Timestamped, Base):
    id: Final[Column[int]] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    fallback_name: Final[Column[str]] = Column(
        String(255),
        CheckConstraint("fallback_name <> ''"),
        nullable=False,
    )

    locales: Final[
        'RelationshipProperty[list[CompanyContactTypeLocaleModel]]'
    ] = relationship(
        'CompanyContactTypeLocaleModel',
        back_populates='type',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    contacts: Final[
        'RelationshipProperty[list[CompanyContactModel]]'
    ] = relationship(
        'CompanyContactModel',
        back_populates='type',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
