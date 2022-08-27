from decimal import Decimal
from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Numeric

from ..._mixins import Timestamped
from ...base_interface import Base
from ...misc.prices.price_model import PriceModel
from .service_model import ServiceModel


class ServicePriceModel(Timestamped, Base):
    service_id: Final[Column[int]] = Column(
        'ServiceId',
        ServiceModel.id.type,
        ForeignKey(ServiceModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
        key='service_id',
    )
    price_id: Final[Column[int]] = Column(
        'PriceId',
        PriceModel.id.type,
        ForeignKey(PriceModel.id, onupdate='CASCADE', ondelete='RESTRICT'),
        primary_key=True,
        key='price_id',
    )
    value: Final[Column[Decimal]] = Column(
        'Value',
        Numeric,
        CheckConstraint('"Value" >= 0'),
        nullable=False,
        key='value',
    )

    service: Final['RelationshipProperty[ServiceModel]'] = relationship(
        'ServiceModel',
        back_populates='prices',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    price: Final['RelationshipProperty[PriceModel]'] = relationship(
        'PriceModel',
        back_populates='services',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
