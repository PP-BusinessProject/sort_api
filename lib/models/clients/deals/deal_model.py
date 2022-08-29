"""The module that provides a `DealModel`."""


from datetime import datetime, timezone
from typing import TYPE_CHECKING, Final, Optional, Type

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy.sql.functions import now
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Integer
from typing_extensions import Self

from ..._mixins import Timestamped
from ...base_interface import Base
from ...misc.prices.price_model import PriceModel
from ..user_model import UserModel

if TYPE_CHECKING:
    from .deal_addition_model import DealAdditionModel


class DealModel(Timestamped, Base):

    user_id: Final[Column[int]] = Column(
        'UserId',
        UserModel.id.type,
        ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        key='user_id',
    )
    id: Final[Column[int]] = Column(
        'Id',
        Integer,
        primary_key=True,
        autoincrement=True,
        key='id',
    )
    fallback_price_id: Final[Column[int]] = Column(
        'FallbackPriceId',
        PriceModel.id.type,
        ForeignKey(PriceModel.id, onupdate='CASCADE', ondelete='RESTRICT'),
        nullable=False,
        key='fallback_price_id',
    )
    fallback_payment_type: Final[Column[bool]] = Column(
        'FallbackPaymentType',
        Boolean(create_constraint=True),
        nullable=False,
        default=False,
        key='fallback_payment_type',
        doc='Prepayment (False) or Payment (True).',
    )
    active_till: Final[Column[Optional[datetime]]] = Column(
        'ActiveTill',
        DateTime(timezone=True),
        key='active_till',
    )

    @hybrid_property
    def is_active(self: Self, /) -> bool:
        return datetime.now(timezone.utc) < self.active_till

    @is_active.expression
    def is_active(cls: Type[Self], /) -> ClauseElement:
        return now() < cls.active_till

    user: Final['RelationshipProperty[UserModel]'] = relationship(
        'UserModel',
        back_populates='deals',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    fallback_price: Final['RelationshipProperty[PriceModel]'] = relationship(
        'PriceModel',
        back_populates='deals',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    additions: Final[
        'RelationshipProperty[list[DealAdditionModel]]'
    ] = relationship(
        'DealAdditionModel',
        back_populates='deal',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
