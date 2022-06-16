from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, SmallInteger, String
from sqlalchemy.sql.expression import literal_column

from .._mixins import Timestamped
from ..base_interface import Base
from ..clients.user_model import UserModel

if TYPE_CHECKING:
    from .bonus_coupon_model import BonusCouponModel
    from .bonus_price_model import BonusPriceModel


class BonusModel(Timestamped, Base):
    owner_id: Final[Column[int]] = Column(
        'OwnerId',
        UserModel.id.type,
        ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        CheckConstraint(
            literal_column('"OwnerId"')
            >= literal_column(str(UserModel.COMPANY_ID))
        ),
        nullable=False,
        key='owner_id',
    )
    id: Final[Column[int]] = Column(
        'Id',
        SmallInteger,
        primary_key=True,
        autoincrement=True,
        key='id',
    )
    name: Final[Column[str]] = Column(
        'Name',
        String(255),
        CheckConstraint('"Name" <> \'\''),
        nullable=False,
        key='name',
    )
    description: Final[Column[str]] = Column(
        'Description',
        String(1023),
        nullable=False,
        default='',
        key='description',
    )
    user_limit: Final[Column[int]] = Column(
        'TotalCount',
        Integer,
        nullable=False,
        default=0,
        key='total_count',
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
