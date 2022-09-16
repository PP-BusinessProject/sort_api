from typing import TYPE_CHECKING, Final, Optional, Type
from uuid import UUID

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.elements import ClauseElement
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean
from typing_extensions import Self

from ...._mixins import Timestamped
from ....base_interface import Base
from ....people.person_model import PersonModel
from ..company_group_model import CompanyGroupModel

if TYPE_CHECKING:
    from ....containers.tanks.operations.openings.container_tank_company_opening_model import (
        ContainerTankCompanyOpeningModel,
    )
    from .company_group_member_right_model import CompanyGroupMemberRightModel


class CompanyGroupMemberModel(Timestamped, Base):

    group_owner_id: Final[Column[UUID]] = Column(
        CompanyGroupModel.owner_id.type,
        ForeignKey(
            CompanyGroupModel.owner_id,
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        primary_key=True,
    )
    person_id: Final[Column[UUID]] = Column(
        PersonModel.user_id.type,
        ForeignKey(
            PersonModel.user_id,
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        primary_key=True,
    )
    accepted: Final[Column[Optional[bool]]] = Column(
        Boolean(create_constraint=True),
    )

    group: Final['RelationshipProperty[CompanyGroupModel]'] = relationship(
        'CompanyGroupModel',
        back_populates='members',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    rights: Final[
        'RelationshipProperty[list[CompanyGroupMemberRightModel]]'
    ] = relationship(
        'CompanyGroupMemberRightModel',
        back_populates='member',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    openings: Final[
        'RelationshipProperty[list[ContainerTankCompanyOpeningModel]]'
    ] = relationship(
        'ContainerTankCompanyOpeningModel',
        back_populates='group_member',
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
