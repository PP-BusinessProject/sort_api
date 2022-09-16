"""The module that provides a `DealModel`."""


from datetime import datetime, timezone
from typing import TYPE_CHECKING, Final, Optional, Type
from uuid import UUID

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
from ..company_model import CompanyModel

if TYPE_CHECKING:
    from .additions.company_deal_addition_model import CompanyDealAdditionModel


class CompanyDealModel(Timestamped, Base):

    company_id: Final[Column[UUID]] = Column(
        CompanyModel.user_id.type,
        ForeignKey(
            CompanyModel.user_id, onupdate='CASCADE', ondelete='CASCADE'
        ),
        nullable=False,
    )
    id: Final[Column[int]] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    fallback_price_id: Final[Column[int]] = Column(
        PriceModel.id.type,
        ForeignKey(PriceModel.id, onupdate='CASCADE', ondelete='RESTRICT'),
        nullable=False,
    )
    fallback_payment_type: Final[Column[bool]] = Column(
        Boolean(create_constraint=True),
        nullable=False,
        default=False,
        doc='Prepayment (False) or Payment (True).',
    )
    active_till: Final[Column[Optional[datetime]]] = Column(
        DateTime(timezone=True),
    )

    @hybrid_property
    def is_active(self: Self, /) -> bool:
        return datetime.now(timezone.utc) < self.active_till

    @is_active.expression
    def is_active(cls: Type[Self], /) -> ClauseElement:
        return now() < cls.active_till

    company: Final['RelationshipProperty[CompanyModel]'] = relationship(
        'CompanyModel',
        back_populates='deals',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    fallback_price: Final['RelationshipProperty[PriceModel]'] = relationship(
        'PriceModel',
        back_populates='company_deals',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    additions: Final[
        'RelationshipProperty[list[CompanyDealAdditionModel]]'
    ] = relationship(
        'CompanyDealAdditionModel',
        back_populates='deal',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
