from decimal import Decimal
from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Numeric

from .._mixins import Timestamped
from ..base_interface import Base
from ..misc.prices.price_model import PriceModel
from .bonus_model import BonusModel


class BonusPriceModel(Timestamped, Base):
    bonus_id: Final[Column[int]] = Column(
        BonusModel.id.type,
        ForeignKey(BonusModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
    )
    price_id: Final[Column[int]] = Column(
        PriceModel.id.type,
        ForeignKey(PriceModel.id, onupdate='CASCADE', ondelete='RESTRICT'),
        primary_key=True,
    )
    value: Final[Column[Decimal]] = Column(
        Numeric(8, 2),
        CheckConstraint('value >= 0'),
        nullable=False,
    )

    bonus: Final['RelationshipProperty[BonusModel]'] = relationship(
        'BonusModel',
        back_populates='prices',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    price: Final['RelationshipProperty[PriceModel]'] = relationship(
        'PriceModel',
        back_populates='bonuses',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
