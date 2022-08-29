from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from ..._mixins import Timestamped
from ...base_interface import Base
from .bonus_coupon_model import BonusCouponModel


class BonusCouponUseModel(Timestamped, Base):
    coupon_id: Final[Column[int]] = Column(
        'CouponId',
        BonusCouponModel.id.type,
        ForeignKey(
            BonusCouponModel.id,
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        nullable=False,
        key='coupon_id',
    )
    id: Final[Column[int]] = Column(
        'Id',
        Integer,
        primary_key=True,
        autoincrement=True,
        key='id',
    )
    amount: Final[Column[int]] = Column(
        'Amount',
        Integer,
        CheckConstraint('"Amount" > 0'),
        nullable=False,
        default=1,
        key='amount',
    )

    coupon: Final['RelationshipProperty[BonusCouponModel]'] = relationship(
        'BonusCouponModel',
        back_populates='uses',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
