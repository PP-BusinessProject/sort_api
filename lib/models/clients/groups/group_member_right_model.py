from typing import Any, Dict, Final, Tuple, Union

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import (
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    SchemaItem,
)

from ..._mixins import Timestamped
from ...base_interface import Base
from .group_member_model import GroupMemberModel
from .group_right_model import GroupRightModel


class GroupMemberRightModel(Timestamped, Base):
    group_owner_id: Final[Column[int]] = Column(
        GroupMemberModel.group_owner_id.type,
        primary_key=True,
    )
    user_id: Final[Column[int]] = Column(
        GroupMemberModel.user_id.type,
        primary_key=True,
    )
    right_id: Final[Column[int]] = Column(
        GroupRightModel.id.type,
        ForeignKey(
            GroupRightModel.id,
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
        primary_key=True,
    )

    member: Final['RelationshipProperty[GroupMemberModel]'] = relationship(
        'GroupMemberModel',
        back_populates='rights',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    right: Final['RelationshipProperty[GroupRightModel]'] = relationship(
        'GroupRightModel',
        back_populates='members',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )

    __table_args__: Final[Tuple[Union[SchemaItem, Dict[str, Any]]]] = (
        ForeignKeyConstraint(
            [group_owner_id, user_id],
            [GroupMemberModel.group_owner_id, GroupMemberModel.user_id],
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
    )
