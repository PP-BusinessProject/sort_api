from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column
from sqlalchemy.sql.sqltypes import Integer, String

from ..._mixins import Timestamped
from ...base_interface import Base

if TYPE_CHECKING:
    from ...bonuses.bonus_price_model import BonusPriceModel
    from ...clients.services.service_price_model import ServicePriceModel
    from ...clients.deals.deal_model import DealModel
    from .price_locale_model import PriceLocaleModel


class PriceModel(Timestamped, Base):
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
        'RelationshipProperty[list[PriceLocaleModel]]'
    ] = relationship(
        'PriceLocaleModel',
        back_populates='price',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    deals: Final['RelationshipProperty[list[DealModel]]'] = relationship(
        'DealModel',
        back_populates='price',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    bonuses: Final[
        'RelationshipProperty[list[BonusPriceModel]]'
    ] = relationship(
        'BonusPriceModel',
        back_populates='price',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    services: Final[
        'RelationshipProperty[list[ServicePriceModel]]'
    ] = relationship(
        'ServicePriceModel',
        back_populates='price',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
