"""The module that provides a `GroupModel`."""


from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, SmallInteger

from .._mixins import Timestamped
from ..base_interface import Base
from .user_model import UserModel


class PersonModel(Timestamped, Base):
    """
    The model that represents a group of users.

    Parameters:
        id (``int``):
            The id of this user.

        created_at (``datetime``):
            The date and time this model was added to the database.

        updated_at (``datetime``):
            The date and time of the last time this model was updated in the
            database.
    """

    user_id: Final[Column[int]] = Column(
        'UserId',
        UserModel.id.type,
        ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
        key='user_id',
    )
    gender: Final[Column[bool]] = Column(
        'Gender',
        Boolean(create_constraint=True),
        nullable=False,
        default=False,
        key='gender',
    )
    family_count: Final[Column[int]] = Column(
        'FamilyCount',
        SmallInteger,
        CheckConstraint('"FamilyCount" >= 1'),
        nullable=False,
        default=1,
        key='family_count',
    )

    user: Final['RelationshipProperty[UserModel]'] = relationship(
        'UserModel',
        back_populates='person',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
