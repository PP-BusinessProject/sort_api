from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Final, Optional

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, Integer, Numeric, DateTime

from .._mixins import Timestamped
from ..base_interface import Base
from ..clients.user_model import UserModel
from ..misc.addresses.address_model import AddressModel

if TYPE_CHECKING:
    from .delivery_service_model import DeliveryServiceModel


class DeliveryModel(Timestamped, Base):

    id: Final[Column[int]] = Column(
        'Id',
        Integer,
        primary_key=True,
        autoincrement=True,
        key='id',
    )
    user_id: Final[Column[int]] = Column(
        'UserId',
        UserModel.id.type,
        ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='NO ACTION'),
        nullable=False,
        key='user_id',
    )
    driver_id: Final[Column[Optional[int]]] = Column(
        'OwnerId',
        UserModel.id.type,
        ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='NO ACTION'),
        key='owner_id',
    )
    latitude: Final[Column[Decimal]] = Column(
        'Latitude',
        Numeric(8, 6),
        nullable=False,
        key='latitude',
    )
    longtitude: Final[Column[Decimal]] = Column(
        'Longtitude',
        Numeric(9, 6),
        nullable=False,
        key='longtitude',
    )
    address_id: Final[Column[Optional[int]]] = Column(
        'AddressId',
        AddressModel.id.type,
        ForeignKey(AddressModel.id, onupdate='CASCADE', ondelete='RESTRICT'),
        key='address_id',
    )
    timestamp: Final[Column[Optional[datetime]]] = Column(
        'Timestamp',
        DateTime(timezone=True),
        key='timestamp',
    )
    success: Final[Column[Optional[bool]]] = Column(
        'Success',
        Boolean(create_constraint=True),
        key='success',
    )

    address: Final['RelationshipProperty[AddressModel]'] = relationship(
        'AddressModel',
        back_populates='deliveries',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    services: Final[
        'RelationshipProperty[list[DeliveryServiceModel]]'
    ] = relationship(
        'DeliveryServiceModel',
        back_populates='delivery',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
