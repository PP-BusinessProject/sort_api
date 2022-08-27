from datetime import timedelta
from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey, CheckConstraint
from sqlalchemy.sql.sqltypes import Integer, SmallInteger, Interval, String

from ..._mixins import Timestamped
from ...base_interface import Base
from ...misc.measurements.measurement_model import MeasurementModel

if TYPE_CHECKING:
    from .container_tank_model import ContainerTankModel
    from .container_tank_type_locale_model import ContainerTankTypeLocaleModel


class ContainerTankTypeModel(Timestamped, Base):
    id: Final[Column[int]] = Column(
        'Id',
        SmallInteger,
        primary_key=True,
        autoincrement=True,
        key='id',
    )
    fallback_name: Final[Column[str]] = Column(
        'FallbackName',
        String(255),
        CheckConstraint('"FallbackName" <> \'\''),
        nullable=False,
        key='name_key',
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
    volume: Final[Column[int]] = Column(
        'Volume',
        Integer,
        nullable=False,
        key='volume',
    )
    clearing_period: Final[Column[timedelta]] = Column(
        'ClearingPeriod',
        Interval(second_precision=True),
        nullable=False,
        default=timedelta(),
        key='clearing_period',
    )

    locales: Final[
        'RelationshipProperty[list[ContainerTankTypeLocaleModel]]'
    ] = relationship(
        'ContainerTankTypeLocaleModel',
        back_populates='type',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    measurement: Final[
        'RelationshipProperty[MeasurementModel]'
    ] = relationship(
        'MeasurementModel',
        back_populates='container_tank_types',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    tanks: Final[
        'RelationshipProperty[list[ContainerTankModel]]'
    ] = relationship(
        'ContainerTankModel',
        back_populates='type',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
