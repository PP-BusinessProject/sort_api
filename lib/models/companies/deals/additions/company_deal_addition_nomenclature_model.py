from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from ...._mixins import Timestamped
from ....base_interface import Base
from ....nomenclatures.nomenclature_model import NomenclatureModel
from .company_deal_addition_model import CompanyDealAdditionModel

if TYPE_CHECKING:
    from ....containers.tanks.operations.openings.container_tank_company_opening_model import (
        ContainerTankCompanyOpeningModel,
    )


class CompanyDealAdditionNomenclatureModel(Timestamped, Base):
    addition_id: Final[Column[int]] = Column(
        CompanyDealAdditionModel.id.type,
        ForeignKey(
            CompanyDealAdditionModel.id,
            onupdate='CASCADE',
            ondelete='CASCADE',
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

    addition: Final[
        'RelationshipProperty[CompanyDealAdditionModel]'
    ] = relationship(
        'CompanyDealAdditionModel',
        back_populates='nomenclatures',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    nomenclature: Final[
        'RelationshipProperty[NomenclatureModel]'
    ] = relationship(
        'NomenclatureModel',
        back_populates='company_deal_additions',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    openings: Final[
        'RelationshipProperty[list[ContainerTankCompanyOpeningModel]]'
    ] = relationship(
        'ContainerTankCompanyOpeningModel',
        back_populates='nomenclature',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
