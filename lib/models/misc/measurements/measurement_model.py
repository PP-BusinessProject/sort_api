from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column
from sqlalchemy.sql.sqltypes import Integer, String

from ..._mixins import Timestamped
from ...base_interface import Base

if TYPE_CHECKING:
    from ...companies.bonuses.company_bonus_model import CompanyBonusModel
    from ...containers.tanks.container_tank_type_model import (
        ContainerTankTypeModel,
    )
    from ...nomenclatures.nomenclature_model import NomenclatureModel
    from .measurement_locale_model import MeasurementLocaleModel


class MeasurementModel(Timestamped, Base):
    id: Final[Column[int]] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    fallback_name: Final[Column[str]] = Column(
        String(255),
        CheckConstraint("fallback_name <> ''"),
        nullable=False,
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
    company_bonuses: Final[
        'RelationshipProperty[list[CompanyBonusModel]]'
    ] = relationship(
        'CompanyBonusModel',
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
    nomenclatures: Final[
        'RelationshipProperty[list[NomenclatureModel]]'
    ] = relationship(
        'NomenclatureModel',
        back_populates='measurement',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
