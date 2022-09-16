"""The module that provides a `GroupModel`."""


from datetime import date
from typing import TYPE_CHECKING, Final, Optional
from uuid import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, Date, SmallInteger, String
from typing_extensions import Self

from .._mixins import Timestamped
from ..auth.user_model import UserModel
from ..base_interface import Base

if TYPE_CHECKING:
    from ..companies.bonuses.coupons.company_bonus_coupon_model import (
        CompanyBonusCouponModel,
    )
    from .deals.person_deal_model import PersonDealModel
    from .person_image_model import PersonImageModel
    from .person_locale_model import PersonLocaleModel
    from ..containers.tanks.operations.openings.container_tank_person_opening_model import (
        ContainerTankPersonOpeningModel,
    )


class PersonModel(Timestamped, Base):

    user_id: Final[Column[UUID]] = Column(
        UserModel.id.type,
        ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
    )

    fallback_first_name: Final[Column[str]] = Column(
        String(64),
        CheckConstraint("fallback_first_name <> ''"),
        nullable=False,
    )
    fallback_last_name: Final[Column[str]] = Column(
        String(64),
        nullable=False,
        default='',
    )
    fallback_middle_name: Final[Column[str]] = Column(
        String(64),
        nullable=False,
        default='',
    )

    birthday: Final[Column[Optional[date]]] = Column(Date)
    gender: Final[Column[bool]] = Column(
        Boolean(create_constraint=True),
        nullable=False,
        default=False,
    )
    family_count: Final[Column[int]] = Column(
        SmallInteger,
        CheckConstraint('family_count >= 1'),
        nullable=False,
        default=1,
    )
    refferal_id: Final[Column[Optional[int]]] = Column(
        user_id.type,
        ForeignKey(user_id, onupdate='CASCADE', ondelete='CASCADE'),
    )

    locales: Final[
        'RelationshipProperty[list[PersonLocaleModel]]'
    ] = relationship(
        'PersonLocaleModel',
        back_populates='person',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    images: Final[
        'RelationshipProperty[list[PersonImageModel]]'
    ] = relationship(
        'PersonImageModel',
        back_populates='person',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )

    user: Final['RelationshipProperty[UserModel]'] = relationship(
        'UserModel',
        back_populates='person',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    refferal: Final['RelationshipProperty[Optional[Self]]'] = relationship(
        'PersonModel',
        back_populates='refferals',
        lazy='noload',
        cascade='save-update',
        remote_side=[user_id],
        uselist=False,
    )
    refferals: Final['RelationshipProperty[list[Self]]'] = relationship(
        'PersonModel',
        back_populates='refferal',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )

    coupons: Final[
        'RelationshipProperty[list[CompanyBonusCouponModel]]'
    ] = relationship(
        'CompanyBonusCouponModel',
        back_populates='owner',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    deals: Final['RelationshipProperty[list[PersonDealModel]]'] = relationship(
        'PersonDealModel',
        back_populates='person',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    openings: Final[
        'RelationshipProperty[list[ContainerTankPersonOpeningModel]]'
    ] = relationship(
        'ContainerTankPersonOpeningModel',
        back_populates='person',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
