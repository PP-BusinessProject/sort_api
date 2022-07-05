from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.expression import and_, literal_column
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, String

from .._mixins import Timestamped
from ..base_interface import Base
from ..clients.user_model import UserModel
from .bonus_model import BonusModel


class BonusCouponModel(Timestamped, Base):
    bonus_id: Final[Column[int]] = Column(
        'BonusId',
        BonusModel.id.type,
        ForeignKey(BonusModel.id, onupdate='CASCADE', ondelete='RESTRICT'),
        primary_key=True,
        key='bonus_id',
    )
    hash: Final[Column[str]] = Column(
        'Hash',
        String(64),
        nullable=False,
        key='hash',
    )
    active: Final[Column[bool]] = Column(
        'Active',
        Boolean(create_constraint=True),
        nullable=False,
        default=True,
        key='active',
    )
    owner_id: Final[Column[int]] = Column(
        'OwnerId',
        UserModel.id.type,
        ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        CheckConstraint(
            and_(
                literal_column(str(UserModel.COMPANY_ID))
                > literal_column('"OwnerId"'),
                literal_column('"OwnerId"') > literal_column('0'),
            )
        ),
        nullable=False,
        key='owner_id',
    )

    bonus: Final['RelationshipProperty[BonusModel]'] = relationship(
        'BonusModel',
        back_populates='coupons',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
