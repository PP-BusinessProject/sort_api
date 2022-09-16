"""The module that provides a `DealModel`."""


from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, Integer

from ...._mixins import Timestamped
from ....base_interface import Base
from ....misc.prices.price_model import PriceModel
from ..company_deal_model import CompanyDealModel

if TYPE_CHECKING:
    from .company_deal_addition_nomenclature_model import (
        CompanyDealAdditionNomenclatureModel,
    )


class CompanyDealAdditionModel(Timestamped, Base):

    deal_id: Final[Column[int]] = Column(
        CompanyDealModel.id.type,
        ForeignKey(
            CompanyDealModel.id,
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        nullable=False,
    )
    id: Final[Column[int]] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    price_id: Final[Column[int]] = Column(
        PriceModel.id.type,
        ForeignKey(PriceModel.id, onupdate='CASCADE', ondelete='RESTRICT'),
        nullable=False,
    )
    payment_type: Final[Column[bool]] = Column(
        Boolean(create_constraint=True),
        nullable=False,
        default=False,
        doc='Prepayment (False) or Payment (True).',
    )

    deal: Final['RelationshipProperty[CompanyDealModel]'] = relationship(
        'CompanyDealModel',
        back_populates='additions',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    price: Final['RelationshipProperty[PriceModel]'] = relationship(
        'PriceModel',
        back_populates='company_deal_additions',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    nomenclatures: Final[
        'RelationshipProperty[list[CompanyDealAdditionNomenclatureModel]]'
    ] = relationship(
        'CompanyDealAdditionNomenclatureModel',
        back_populates='addition',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
