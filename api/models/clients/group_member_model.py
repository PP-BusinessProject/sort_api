"""The module that provides a `GroupModel`."""


from enum import IntFlag, auto
from typing import Final, Optional, Type

from sqlalchemy import CheckConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.elements import ClauseElement
from sqlalchemy.sql.expression import and_, literal_column
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean
from typing_extensions import Self

from .._mixins import Timestamped
from .._types import IntEnumType
from ..base_interface import Base
from .group_model import GroupModel
from .user_model import UserModel


class GroupRights(IntFlag):
    """The rights provided for a `GroupMemberModel` in a `GroupModel`."""

    OPEN_CONTAINERS: Final[int] = auto()
    SCAN_BONUSES: Final[int] = auto()
    EDIT_BONUSES: Final[int] = auto()
    MANAGE_MEMBERS: Final[int] = auto()


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
        'GroupOwnerId',
        GroupModel.owner_id.type,
        ForeignKey(
            GroupModel.owner_id,
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        primary_key=True,
        key='group_owner_id',
    )
    user_id: Final[Column[int]] = Column(
        'UserId',
        UserModel.id.type,
        ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        CheckConstraint(
            and_(
                literal_column(str(UserModel.COMPANY_ID))
                > literal_column('"UserId"'),
                literal_column('"UserId"') > literal_column('0'),
            )
        ),
        primary_key=True,
        key='user_id',
    )
    accepted: Final[Column[Optional[bool]]] = Column(
        'Accepted',
        Boolean(create_constraint=True),
        key='accepted',
    )
    rights: Final[Column[GroupRights]] = Column(
        'Rights',
        IntEnumType(GroupRights),
        default=GroupRights.OPEN_CONTAINERS,
        nullable=False,
        key='rights',
    )

    group: Final['RelationshipProperty[GroupModel]'] = relationship(
        'GroupModel',
        back_populates='members',
        lazy='noload',
        cascade='save-update',
        uselist=False,
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
        return cls.accepted.is_(False)
