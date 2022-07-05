from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from ..base_interface import Base
from .address_model import AddressModel

if TYPE_CHECKING:
    from ..clients.company_model import CompanyModel


class BankModel(Base):
    code: Final[Column[int]] = Column(
        'Code',
        Integer,
        primary_key=True,
        key='code',
    )
    name: Final[Column[str]] = Column(
        'Name',
        String(255),
        nullable=False,
        key='name',
    )
    address_id: Final[Column[AddressModel]] = Column(
        'AddressId',
        AddressModel.id.type,
        ForeignKey(AddressModel.id, onupdate='CASCADE', ondelete='RESTRICT'),
        nullable=False,
        key='address_id',
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
