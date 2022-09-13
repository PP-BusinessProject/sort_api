from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey, CheckConstraint
from sqlalchemy.sql.sqltypes import Integer, String

from ...base_interface import Base
from ..addresses.address_model import AddressModel

if TYPE_CHECKING:
    from ...clients.companies.company_model import CompanyModel
    from .bank_locale_model import BankLocaleModel


class BankModel(Base):
    code: Final[Column[int]] = Column(
        Integer,
        primary_key=True,
    )
    fallback_name: Final[Column[str]] = Column(
        String(255),
        CheckConstraint("fallback_name <> ''"),
        nullable=False,
    )
    address_id: Final[Column[AddressModel]] = Column(
        AddressModel.id.type,
        ForeignKey(AddressModel.id, onupdate='CASCADE', ondelete='RESTRICT'),
        nullable=False,
    )

    locales: Final[
        'RelationshipProperty[list[BankLocaleModel]]'
    ] = relationship(
        'BankLocaleModel',
        back_populates='bank',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    address: Final['RelationshipProperty[AddressModel]'] = relationship(
        'AddressModel',
        back_populates='banks',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    companies: Final['RelationshipProperty[CompanyModel]'] = relationship(
        'CompanyModel',
        back_populates='bank',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
