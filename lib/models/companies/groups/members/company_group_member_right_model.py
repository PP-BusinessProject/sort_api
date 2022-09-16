from typing import Any, Dict, Final, Tuple, Union

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import (
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    SchemaItem,
)

from ...._mixins import Timestamped
from ....base_interface import Base
from ..rights.company_group_right_model import CompanyGroupRightModel
from .company_group_member_model import CompanyGroupMemberModel


class CompanyGroupMemberRightModel(Timestamped, Base):
    group_owner_id: Final[Column[int]] = Column(
        CompanyGroupMemberModel.group_owner_id.type,
        primary_key=True,
    )
    person_id: Final[Column[int]] = Column(
        CompanyGroupMemberModel.person_id.type,
        primary_key=True,
    )
    right_id: Final[Column[int]] = Column(
        CompanyGroupRightModel.id.type,
        ForeignKey(
            CompanyGroupRightModel.id,
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
        primary_key=True,
    )

    member: Final[
        'RelationshipProperty[CompanyGroupMemberModel]'
    ] = relationship(
        'CompanyGroupMemberModel',
        back_populates='rights',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    right: Final[
        'RelationshipProperty[CompanyGroupRightModel]'
    ] = relationship(
        'CompanyGroupRightModel',
        back_populates='members',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )

    __table_args__: Final[Tuple[Union[SchemaItem, Dict[str, Any]]]] = (
        ForeignKeyConstraint(
            [group_owner_id, person_id],
            [
                CompanyGroupMemberModel.group_owner_id,
                CompanyGroupMemberModel.person_id,
            ],
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
    )
