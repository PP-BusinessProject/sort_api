from datetime import datetime
from typing import TYPE_CHECKING, Final, Optional

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Integer

from ...._mixins import Timestamped
from ....base_interface import Base
from ....people.person_model import PersonModel
from ..company_bonus_model import CompanyBonusModel

if TYPE_CHECKING:
    from .company_bonus_coupon_use_model import CompanyBonusCouponUseModel


class CompanyBonusCouponModel(Timestamped, Base):
    bonus_id: Final[Column[int]] = Column(
        CompanyBonusModel.id.type,
        ForeignKey(
            CompanyBonusModel.id, onupdate='CASCADE', ondelete='RESTRICT'
        ),
        nullable=False,
    )

    id: Final[Column[int]] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    count: Final[Column[int]] = Column(
        Integer,
        CheckConstraint('count > 0'),
        nullable=False,
        default=1,
    )
    active_till: Final[Column[Optional[datetime]]] = Column(
        DateTime(timezone=True),
    )
    owner_id: Final[Column[Optional[int]]] = Column(
        PersonModel.user_id.type,
        ForeignKey(
            PersonModel.user_id, onupdate='CASCADE', ondelete='SET NULL'
        ),
    )

    bonus: Final['RelationshipProperty[CompanyBonusModel]'] = relationship(
        'CompanyBonusModel',
        back_populates='coupons',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    owner: Final['RelationshipProperty[Optional[PersonModel]]'] = relationship(
        'PersonModel',
        back_populates='coupons',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    uses: Final[
        'RelationshipProperty[list[CompanyBonusCouponUseModel]]'
    ] = relationship(
        'CompanyBonusCouponUseModel',
        back_populates='coupon',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
