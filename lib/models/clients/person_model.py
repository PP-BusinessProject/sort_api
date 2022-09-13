"""The module that provides a `GroupModel`."""


from typing import Final, Optional
from sqlalchemy.sql.expression import and_
from sqlalchemy.sql.elements import literal_column

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, SmallInteger

from .._mixins import Timestamped
from ..base_interface import Base
from .user_model import UserModel


class PersonModel(Timestamped, Base):

    refferal_id: Final[Column[Optional[int]]] = Column(
        UserModel.id.type,
        ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        CheckConstraint(
            and_(
                literal_column(str(UserModel.COMPANY_ID))
                > literal_column('refferal_id'),
                literal_column('refferal_id') > literal_column('0'),
            )
        ),
    )
    user_id: Final[Column[int]] = Column(
        UserModel.id.type,
        ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
    )
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

    user: Final['RelationshipProperty[UserModel]'] = relationship(
        'UserModel',
        back_populates='person',
        lazy='noload',
        cascade='save-update',
        foreign_keys=[user_id],
        uselist=False,
    )
    refferal: Final[
        'RelationshipProperty[Optional[UserModel]]'
    ] = relationship(
        'UserModel',
        back_populates='refferals',
        lazy='noload',
        cascade='save-update',
        foreign_keys=[refferal_id],
        uselist=False,
    )
