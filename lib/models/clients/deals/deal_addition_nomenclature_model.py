from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from ..._mixins import Timestamped
from ...base_interface import Base
from ...nomenclatures.nomenclature_model import NomenclatureModel
from .deal_addition_model import DealAdditionModel

if TYPE_CHECKING:
    from ...containers.tanks.operations.container_tank_opening_model import (
        ContainerTankOpeningModel,
    )


class DealAdditionNomenclatureModel(Timestamped, Base):
    addition_id: Final[Column[int]] = Column(
        DealAdditionModel.id.type,
        ForeignKey(
            DealAdditionModel.id, onupdate='CASCADE', ondelete='CASCADE'
        ),
        primary_key=True,
    )
    nomenclature_id: Final[Column[int]] = Column(
        NomenclatureModel.id.type,
        ForeignKey(
            NomenclatureModel.id, onupdate='CASCADE', ondelete='RESTRICT'
        ),
        primary_key=True,
    )
    amount: Final[Column[int]] = Column(
        Integer,
        CheckConstraint('amount > 0'),
        nullable=False,
        default=1,
    )

    addition: Final['RelationshipProperty[DealAdditionModel]'] = relationship(
        'DealAdditionModel',
        back_populates='nomenclatures',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    nomenclature: Final[
        'RelationshipProperty[NomenclatureModel]'
    ] = relationship(
        'NomenclatureModel',
        back_populates='deal_additions',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    openings: Final[
        'RelationshipProperty[list[ContainerTankOpeningModel]]'
    ] = relationship(
        'ContainerTankOpeningModel',
        back_populates='nomenclature',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
