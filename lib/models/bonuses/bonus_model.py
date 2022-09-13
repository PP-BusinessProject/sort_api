from datetime import datetime
from typing import TYPE_CHECKING, Final, Optional

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.expression import literal_column
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Integer, String

from .._mixins import Timestamped
from ..base_interface import Base
from ..clients.user_model import UserModel
from ..misc.measurements.measurement_model import MeasurementModel
from .categories.bonus_category_model import BonusCategoryModel

if TYPE_CHECKING:

    from .bonus_image_model import BonusImageModel
    from .bonus_locale_model import BonusLocaleModel
    from .bonus_price_model import BonusPriceModel
    from .coupons.bonus_coupon_model import BonusCouponModel


class BonusModel(Timestamped, Base):
    owner_id: Final[Column[int]] = Column(
        UserModel.id.type,
        ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        CheckConstraint(
            literal_column('owner_id')
            >= literal_column(str(UserModel.COMPANY_ID))
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
        BonusCategoryModel.id.type,
        ForeignKey(
            BonusCategoryModel.id,
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

    owner: Final['RelationshipProperty[UserModel]'] = relationship(
        'UserModel',
        back_populates='bonuses',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    locales: Final[
        'RelationshipProperty[list[BonusLocaleModel]]'
    ] = relationship(
        'BonusLocaleModel',
        back_populates='bonus',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    images: Final[
        'RelationshipProperty[list[BonusImageModel]]'
    ] = relationship(
        'BonusImageModel',
        back_populates='bonus',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    category: Final['RelationshipProperty[BonusCategoryModel]'] = relationship(
        'BonusCategoryModel',
        back_populates='bonuses',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    measurement: Final[
        'RelationshipProperty[MeasurementModel]'
    ] = relationship(
        'MeasurementModel',
        back_populates='bonuses',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    coupons: Final[
        'RelationshipProperty[list[BonusCouponModel]]'
    ] = relationship(
        'BonusCouponModel',
        back_populates='bonus',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    prices: Final[
        'RelationshipProperty[list[BonusPriceModel]]'
    ] = relationship(
        'BonusPriceModel',
        back_populates='bonus',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
