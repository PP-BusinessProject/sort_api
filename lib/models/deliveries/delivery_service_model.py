from decimal import Decimal
from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Numeric

from .._mixins import Timestamped
from ..base_interface import Base
from ..clients.service_model import ServiceModel
from .delivery_model import DeliveryModel


class DeliveryServiceModel(Timestamped, Base):
    delivery_id: Final[Column[int]] = Column(
        'UserId',
        DeliveryModel.id.type,
        ForeignKey(DeliveryModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
        key='user_id',
    )
    service_id: Final[Column[int]] = Column(
        'ServiceId',
        ServiceModel.id.type,
        ForeignKey(ServiceModel.id, onupdate='CASCADE', ondelete='RESTRICT'),
        primary_key=True,
        key='service_id',
    )
    amount: Final[Column[Decimal]] = Column(
        'Amount',
        Numeric,
        CheckConstraint('"Amount" > 0'),
        nullable=False,
        default=1,
        key='amount',
    )

    delivery: Final[
        'RelationshipProperty[list[DeliveryModel]]'
    ] = relationship(
        'DeliveryModel',
        back_populates='services',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    service: Final['RelationshipProperty[list[ServiceModel]]'] = relationship(
        'ServiceModel',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
