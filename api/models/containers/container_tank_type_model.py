from datetime import timedelta
from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, SmallInteger, String

from .._mixins import Timestamped
from .._types import TimeDelta
from ..base_interface import Base
from ..misc.measurement_model import MeasurementModel

if TYPE_CHECKING:
    from .container_tank_model import ContainerTankModel


class ContainerTankTypeModel(Timestamped, Base):
    id: Final[Column[int]] = Column(
        'Id',
        SmallInteger,
        primary_key=True,
        autoincrement=True,
        key='id',
    )
    name: Final[Column[str]] = Column(
        'Name',
        String,
        nullable=False,
        key='name',
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
        TimeDelta,
        nullable=False,
        default=timedelta(),
        key='clearing_period',
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
