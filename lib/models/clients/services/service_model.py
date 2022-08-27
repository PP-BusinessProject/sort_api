from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from ...base_interface import Base
from ...misc.measurements.measurement_model import MeasurementModel

if TYPE_CHECKING:
    from ..deals.deal_service_model import DealServiceModel
    from .service_price_model import ServicePriceModel
    from .service_locale_model import ServiceLocaleModel


class ServiceModel(Base):
    id: Final[Column[int]] = Column(
        'Id',
        Integer,
        primary_key=True,
        autoincrement=True,
        key='id',
    )
    fallback_name: Final[Column[str]] = Column(
        'FallbackName',
        String(255),
        CheckConstraint('"FallbackName" <> \'\''),
        nullable=False,
        key='fallback_name',
    )
    fallback_description: Final[Column[str]] = Column(
        'FallbackDescription',
        String(1023),
        nullable=False,
        key='fallback_description',
    )
    measurement_id: Final[Column[int]] = Column(
        'MeasurementId',
        MeasurementModel.id.type,
        ForeignKey(
            MeasurementModel.id,
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
        nullable=False,
        key='measurement_id',
    )

    locales: Final[
        'RelationshipProperty[list[ServiceLocaleModel]]'
    ] = relationship(
        'ServiceLocaleModel',
        back_populates='service',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    measurement: Final[
        'RelationshipProperty[MeasurementModel]'
    ] = relationship(
        'MeasurementModel',
        back_populates='services',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    prices: Final[
        'RelationshipProperty[list[ServicePriceModel]]'
    ] = relationship(
        'ServicePriceModel',
        back_populates='service',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    deals: Final[
        'RelationshipProperty[list[DealServiceModel]]'
    ] = relationship(
        'DealServiceModel',
        back_populates='service',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
