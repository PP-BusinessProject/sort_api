from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from ...._mixins import Timestamped
from ....base_interface import Base
from .company_bonus_coupon_model import CompanyBonusCouponModel


class CompanyBonusCouponUseModel(Timestamped, Base):
    coupon_id: Final[Column[int]] = Column(
        CompanyBonusCouponModel.id.type,
        ForeignKey(
            CompanyBonusCouponModel.id,
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        nullable=False,
    )
    id: Final[Column[int]] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    amount: Final[Column[int]] = Column(
        Integer,
        CheckConstraint('amount > 0'),
        nullable=False,
        default=1,
    )

    coupon: Final[
        'RelationshipProperty[CompanyBonusCouponModel]'
    ] = relationship(
        'CompanyBonusCouponModel',
        back_populates='uses',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
