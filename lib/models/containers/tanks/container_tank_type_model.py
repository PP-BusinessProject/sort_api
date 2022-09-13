from datetime import timedelta
from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Interval, SmallInteger, String

from ..._mixins import Timestamped
from ...base_interface import Base
from ...misc.measurements.measurement_model import MeasurementModel

if TYPE_CHECKING:
    from .container_tank_model import ContainerTankModel
    from .container_tank_type_locale_model import ContainerTankTypeLocaleModel


class ContainerTankTypeModel(Timestamped, Base):
    id: Final[Column[int]] = Column(
        SmallInteger,
        primary_key=True,
        autoincrement=True,
    )
    fallback_name: Final[Column[str]] = Column(
        String(255),
        CheckConstraint("fallback_name <> ''"),
        nullable=False,
    )
    measurement_id: Final[Column[int]] = Column(
        MeasurementModel.id.type,
        ForeignKey(
            MeasurementModel.id,
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
        nullable=False,
    )
    volume: Final[Column[int]] = Column(
        Integer,
        nullable=False,
    )
    clearing_period: Final[Column[timedelta]] = Column(
        Interval(second_precision=True),
        nullable=False,
        default=timedelta(),
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
