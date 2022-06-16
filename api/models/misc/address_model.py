from typing import TYPE_CHECKING, Final, Optional

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from ..base_interface import Base

if TYPE_CHECKING:
    from ..clients.company_model import CompanyModel
    from ..containers.container_model import ContainerModel
    from ..deliveries.delivery_model import DeliveryModel
    from .bank_model import BankModel


class AddressModel(Base):
    id: Final[Column[int]] = Column(
        'Id',
        Integer,
        primary_key=True,
        autoincrement=True,
        key='id',
    )
    country: Final[Column[str]] = Column(
        'Сountry',
        String,
        nullable=False,
        default='Ukraine',
        key='country',
    )
    state: Final[Column[str]] = Column(
        'State',
        String,
        nullable=False,
        key='state',
    )
    city: Final[Column[str]] = Column(
        'City',
        String,
        nullable=False,
        key='city',
    )
    street: Final[Column[str]] = Column(
        'Street',
        String,
        nullable=False,
        key='street',
    )
    building: Final[Column[int]] = Column(
        'Building',
        Integer,
        nullable=False,
        key='building',
    )
    appartment: Final[Column[Optional[int]]] = Column(
        'Appartment',
        Integer,
        key='appartment',
    )
    postal_code: Final[Column[int]] = Column(
        'PostalCode',
        Integer,
        nullable=False,
        key='postal_code',
    )

    banks: Final['RelationshipProperty[BankModel]'] = relationship(
        'BankModel',
        back_populates='address',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    companies: Final['RelationshipProperty[CompanyModel]'] = relationship(
        'CompanyModel',
        back_populates='address',
        lazy='noload',
        primaryjoin='AddressModel.id == CompanyModel.address_id',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    containers: Final['RelationshipProperty[ContainerModel]'] = relationship(
        'ContainerModel',
        back_populates='address',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    deliveries: Final['RelationshipProperty[DeliveryModel]'] = relationship(
        'DeliveryModel',
        back_populates='address',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
