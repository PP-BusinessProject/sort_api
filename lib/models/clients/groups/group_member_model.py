from typing import TYPE_CHECKING, Final, Optional, Type

from sqlalchemy import CheckConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.elements import ClauseElement
from sqlalchemy.sql.expression import and_, literal_column
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean
from typing_extensions import Self

from ..._mixins import Timestamped
from ...base_interface import Base
from ..user_model import UserModel
from .group_model import GroupModel

if TYPE_CHECKING:
    from .group_member_right_model import GroupMemberRightModel
# @unique
# class GroupRights(IntFlag):
#     """The rights provided for a `GroupMemberModel` in a `GroupModel`."""

#     OPEN_CONTAINERS: Final[int] = auto()
#     SCAN_BONUSES: Final[int] = auto()
#     EDIT_BONUSES: Final[int] = auto()
#     MANAGE_MEMBERS: Final[int] = auto()


class GroupMemberModel(Timestamped, Base):
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

    group_owner_id: Final[Column[int]] = Column(
        GroupModel.owner_id.type,
        ForeignKey(
            GroupModel.owner_id,
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        primary_key=True,
    )
    user_id: Final[Column[int]] = Column(
        UserModel.id.type,
        ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        CheckConstraint(
            and_(
                literal_column(str(UserModel.COMPANY_ID))
                > literal_column('user_id'),
                literal_column('user_id') > literal_column('0'),
            )
        ),
        primary_key=True,
    )
    accepted: Final[Column[Optional[bool]]] = Column(
        Boolean(create_constraint=True),
    )

    group: Final['RelationshipProperty[GroupModel]'] = relationship(
        'GroupModel',
        back_populates='members',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    rights: Final[
        'RelationshipProperty[list[GroupMemberRightModel]]'
    ] = relationship(
        'GroupMemberRightModel',
        back_populates='member',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )

    @hybrid_property
    def banned(self: Self, /) -> bool:  # noqa: D102
        return self.accepted is False

    @banned.setter
    def banned(self: Self, value: bool, /) -> None:
        if not isinstance(value, bool):
            raise ValueError(f'Invalid value: {value}')
        self.accepted = not value

    @banned.expression
    def banned(cls: Type[Self], /) -> ClauseElement:
        # sourcery skip: instance-method-first-arg-name
        return cls.accepted.is_(False)
