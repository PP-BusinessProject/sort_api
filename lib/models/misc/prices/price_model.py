from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column
from sqlalchemy.sql.sqltypes import Integer, String

from ..._mixins import Timestamped
from ...base_interface import Base

if TYPE_CHECKING:
    from ...companies.bonuses.company_bonus_price_model import (
        CompanyBonusPriceModel,
    )
    from ...companies.deals.additions.company_deal_addition_model import (
        CompanyDealAdditionModel,
    )
    from ...companies.deals.company_deal_model import CompanyDealModel
    from ...nomenclatures.nomenclature_price_model import (
        NomenclaturePriceModel,
    )
    from ...people.deals.additions.person_deal_addition_model import (
        PersonDealAdditionModel,
    )
    from ...people.deals.person_deal_model import PersonDealModel
    from .price_locale_model import PriceLocaleModel


class PriceModel(Timestamped, Base):
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
        'RelationshipProperty[list[PriceLocaleModel]]'
    ] = relationship(
        'PriceLocaleModel',
        back_populates='price',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    company_bonuses: Final[
        'RelationshipProperty[list[CompanyBonusPriceModel]]'
    ] = relationship(
        'CompanyBonusPriceModel',
        back_populates='price',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    company_deals: Final[
        'RelationshipProperty[list[CompanyDealModel]]'
    ] = relationship(
        'CompanyDealModel',
        back_populates='fallback_price',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    company_deal_additions: Final[
        'RelationshipProperty[list[CompanyDealAdditionModel]]'
    ] = relationship(
        'CompanyDealAdditionModel',
        back_populates='price',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    nomenclatures: Final[
        'RelationshipProperty[list[NomenclaturePriceModel]]'
    ] = relationship(
        'NomenclaturePriceModel',
        back_populates='price',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    person_deals: Final[
        'RelationshipProperty[list[PersonDealModel]]'
    ] = relationship(
        'PersonDealModel',
        back_populates='fallback_price',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    person_deal_additions: Final[
        'RelationshipProperty[list[PersonDealAdditionModel]]'
    ] = relationship(
        'PersonDealAdditionModel',
        back_populates='price',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
