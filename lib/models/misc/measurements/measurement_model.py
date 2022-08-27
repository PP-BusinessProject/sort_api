from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column
from sqlalchemy.sql.sqltypes import Integer, String

from ..._mixins import Timestamped
from ...base_interface import Base

if TYPE_CHECKING:
    from ...clients.services.service_model import ServiceModel
    from ...containers.tanks.container_tank_type_model import (
        ContainerTankTypeModel,
    )
    from .measurement_locale_model import MeasurementLocaleModel


class MeasurementModel(Timestamped, Base):
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

    locales: Final[
        'RelationshipProperty[list[MeasurementLocaleModel]]'
    ] = relationship(
        'MeasurementLocaleModel',
        back_populates='measurement',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    container_tank_types: Final[
        'RelationshipProperty[list[ContainerTankTypeModel]]'
    ] = relationship(
        'ContainerTankTypeModel',
        back_populates='measurement',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    services: Final['RelationshipProperty[list[ServiceModel]]'] = relationship(
        'ServiceModel',
        back_populates='measurement',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
