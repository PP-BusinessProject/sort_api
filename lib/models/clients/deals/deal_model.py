"""The module that provides a `DealModel`."""


from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING, Final, Type

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy.sql.functions import now
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Integer, Numeric
from typing_extensions import Self

from ..._mixins import Timestamped
from ...base_interface import Base
from ...misc.prices.price_model import PriceModel
from ..user_model import UserModel

if TYPE_CHECKING:
    from .deal_service_model import DealServiceModel


class DealModel(Timestamped, Base):

    owner_id: Final[Column[int]] = Column(
        'OwnerId',
        UserModel.id.type,
        ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        key='owner_id',
    )
    id: Final[Column[int]] = Column(
        'Id',
        Integer,
        primary_key=True,
        autoincrement=True,
        key='id',
    )
    price_id: Final[Column[int]] = Column(
        'PriceId',
        PriceModel.id.type,
        ForeignKey(PriceModel.id, onupdate='CASCADE', ondelete='RESTRICT'),
        nullable=False,
        key='price_id',
    )
    payment_type: Final[Column[bool]] = Column(
        'PaymentType',
        Boolean(create_constraint=True),
        nullable=False,
        default=False,
        key='payment_type',
    )
    refferal_discount: Final[Column[Decimal]] = Column(
        'RefferalDiscount',
        Numeric(8, 8),
        nullable=False,
        default=Decimal(),
        key='refferal_discount',
    )
    active_till: Final[Column[datetime]] = Column(
        'ActiveTill',
        DateTime(timezone=True),
        nullable=False,
        key='active_till',
    )

    @hybrid_property
    def is_active(self: Self, /) -> bool:
        return datetime.now(timezone.utc) < self.active_till

    @is_active.expression
    def is_active(cls: Type[Self], /) -> ClauseElement:
        return now() < cls.active_till

    owner: Final['RelationshipProperty[UserModel]'] = relationship(
        'UserModel',
        back_populates='deals',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    price: Final['RelationshipProperty[PriceModel]'] = relationship(
        'PriceModel',
        back_populates='deals',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    services: Final[
        'RelationshipProperty[list[DealServiceModel]]'
    ] = relationship(
        'DealServiceModel',
        back_populates='deal',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
