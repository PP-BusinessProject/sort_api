from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column
from sqlalchemy.sql.sqltypes import Integer, String

from .._mixins import Timestamped
from ..base_interface import Base

if TYPE_CHECKING:
    from ..bonuses.bonus_price_model import BonusPriceModel
    from ..clients.service_price_model import ServicePriceModel
    from ..clients.deal_model import DealModel


class PriceModel(Timestamped, Base):
    id: Final[Column[int]] = Column(
        'Id',
        Integer,
        primary_key=True,
        autoincrement=True,
        key='id',
    )
    name: Final[Column[str]] = Column(
        'Name',
        String(255),
        CheckConstraint('"Name" <> \'\''),
        nullable=False,
        key='name',
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
