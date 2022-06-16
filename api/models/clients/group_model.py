"""The module that provides a `GroupModel`."""


from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String

from .._mixins import Timestamped
from ..base_interface import Base
from .user_model import UserModel

if TYPE_CHECKING:
    from .group_member_model import GroupMemberModel


class GroupModel(Timestamped, Base):
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

    owner_id: Final[Column[int]] = Column(
        'OwnerId',
        UserModel.id.type,
        ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
        key='owner_id',
    )
    name: Final[Column[str]] = Column(
        'Name',
        String(64),
        nullable=False,
        default='',
        key='name',
    )

    owner: Final['RelationshipProperty[UserModel]'] = relationship(
        'UserModel',
        back_populates='group',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    members: Final[
        'RelationshipProperty[list[GroupMemberModel]]'
    ] = relationship(
        'GroupMemberModel',
        back_populates='group',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
