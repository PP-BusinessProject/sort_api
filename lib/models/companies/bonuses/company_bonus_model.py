from datetime import datetime
from typing import TYPE_CHECKING, Final, Optional
from uuid import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Integer, String

from ..._mixins import Timestamped
from ...base_interface import Base
from ..company_model import CompanyModel
from ...misc.measurements.measurement_model import MeasurementModel
from .categories.company_bonus_category_model import CompanyBonusCategoryModel

if TYPE_CHECKING:

    from .company_bonus_image_model import CompanyBonusImageModel
    from .company_bonus_locale_model import CompanyBonusLocaleModel
    from .company_bonus_price_model import CompanyBonusPriceModel
    from .coupons.company_bonus_coupon_model import CompanyBonusCouponModel


class CompanyBonusModel(Timestamped, Base):
    owner_id: Final[Column[UUID]] = Column(
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

    fallback_name: Final[Column[str]] = Column(
        String(255),
        CheckConstraint("fallback_name <> ''"),
        nullable=False,
    )
    fallback_description: Final[Column[str]] = Column(
        String(1023),
        nullable=False,
        default='',
    )

    category_id: Final[Column[int]] = Column(
        CompanyBonusCategoryModel.id.type,
        ForeignKey(
            CompanyBonusCategoryModel.id,
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
        nullable=False,
    )
    measurement_id: Final[Column[int]] = Column(
        MeasurementModel.id.type,
        ForeignKey(
            MeasurementModel.id,
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
        nullable=False,
    )

    user_limit: Final[Column[int]] = Column(
        Integer,
        CheckConstraint('user_limit >= 0'),
        nullable=False,
        default=0,
        doc='Coupon limit for a single user.',
    )
    active_till: Final[Column[Optional[datetime]]] = Column(
        DateTime(timezone=True),
    )

    company: Final['RelationshipProperty[CompanyModel]'] = relationship(
        'CompanyModel',
        back_populates='bonuses',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    locales: Final[
        'RelationshipProperty[list[CompanyBonusLocaleModel]]'
    ] = relationship(
        'CompanyBonusLocaleModel',
        back_populates='bonus',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    images: Final[
        'RelationshipProperty[list[CompanyBonusImageModel]]'
    ] = relationship(
        'CompanyBonusImageModel',
        back_populates='bonus',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    category: Final[
        'RelationshipProperty[CompanyBonusCategoryModel]'
    ] = relationship(
        'CompanyBonusCategoryModel',
        back_populates='bonuses',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    measurement: Final[
        'RelationshipProperty[MeasurementModel]'
    ] = relationship(
        'MeasurementModel',
        back_populates='company_bonuses',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    coupons: Final[
        'RelationshipProperty[list[CompanyBonusCouponModel]]'
    ] = relationship(
        'CompanyBonusCouponModel',
        back_populates='bonus',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    prices: Final[
        'RelationshipProperty[list[CompanyBonusPriceModel]]'
    ] = relationship(
        'CompanyBonusPriceModel',
        back_populates='bonus',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
