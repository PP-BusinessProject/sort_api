from datetime import datetime
from typing import TYPE_CHECKING, Final, Optional

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.expression import and_, literal_column
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Integer

from ..._mixins import Timestamped
from ...base_interface import Base
from ...clients.user_model import UserModel
from ..bonus_model import BonusModel

if TYPE_CHECKING:
    from .bonus_coupon_use_model import BonusCouponUseModel


class BonusCouponModel(Timestamped, Base):
    bonus_id: Final[Column[int]] = Column(
        BonusModel.id.type,
        ForeignKey(BonusModel.id, onupdate='CASCADE', ondelete='RESTRICT'),
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
        UserModel.id.type,
        ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='SET NULL'),
        CheckConstraint(
            and_(
                literal_column(str(UserModel.COMPANY_ID))
                > literal_column('owner_id'),
                literal_column('owner_id') > literal_column('0'),
            )
        ),
    )

    bonus: Final['RelationshipProperty[BonusModel]'] = relationship(
        'BonusModel',
        back_populates='coupons',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    uses: Final[
        'RelationshipProperty[list[BonusCouponUseModel]]'
    ] = relationship(
        'BonusCouponUseModel',
        back_populates='coupon',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
