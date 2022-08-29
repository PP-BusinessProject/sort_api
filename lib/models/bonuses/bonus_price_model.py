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
        'BonusId',
        BonusModel.id.type,
        ForeignKey(BonusModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
        key='bonus_id',
    )
    price_id: Final[Column[int]] = Column(
        'PriceId',
        PriceModel.id.type,
        ForeignKey(PriceModel.id, onupdate='CASCADE', ondelete='RESTRICT'),
        primary_key=True,
        key='price_id',
    )
    value: Final[Column[Decimal]] = Column(
        'Value',
        Numeric(8, 2),
        CheckConstraint('"Value" >= 0'),
        nullable=False,
        key='value',
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
