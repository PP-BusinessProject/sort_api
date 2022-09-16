from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Final,
    Optional,
    Tuple,
    Type,
    Union,
)
from uuid import UUID

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.elements import ClauseElement
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column, ForeignKeyConstraint, SchemaItem
from sqlalchemy.sql.sqltypes import Integer
from typing_extensions import Self

from ....._mixins import Timestamped
from .....base_interface import Base
from .....companies.deals.additions.company_deal_addition_nomenclature_model import (
    CompanyDealAdditionNomenclatureModel,
)
from .....companies.groups.members.company_group_member_model import (
    CompanyGroupMemberModel,
)
from ...container_tank_model import ContainerTankModel

if TYPE_CHECKING:
    from .container_tank_person_opening_drop_model import (
        ContainerTankCompanyOpeningDropModel,
    )


class ContainerTankCompanyOpeningModel(Timestamped, Base):
    group_owner_id: Final[Column[UUID]] = Column(
        CompanyGroupMemberModel.group_owner_id.type,
        nullable=False,
    )
    group_member_id: Final[Column[int]] = Column(
        CompanyGroupMemberModel.person_id.type,
        nullable=False,
    )
    container_id: Final[Column[int]] = Column(
        ContainerTankModel.container_id.type,
        nullable=False,
    )
    tank_type_id: Final[Column[int]] = Column(
        ContainerTankModel.type_id.type,
        nullable=False,
    )
    addition_id: Final[Column[int]] = Column(
        CompanyDealAdditionNomenclatureModel.addition_id.type,
        nullable=False,
    )
    nomenclature_id: Final[Column[int]] = Column(
        CompanyDealAdditionNomenclatureModel.nomenclature_id.type,
        nullable=False,
    )

    id: Final[Column[int]] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    @hybrid_property
    def volume(self: Self, /) -> int:  # noqa: D102
        return sum(drop.volume for drop in self.drops) if self.drops else 0

    @volume.expression
    def volume(cls: Type[Self], /) -> ClauseElement:
        return func.sum(
            ContainerTankCompanyOpeningDropModel.volume
        ).select_from(cls.drops)

    group_member: Final[
        'RelationshipProperty[CompanyGroupMemberModel]'
    ] = relationship(
        'CompanyGroupMemberModel',
        back_populates='openings',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    tank: Final['RelationshipProperty[ContainerTankModel]'] = relationship(
        'ContainerTankModel',
        back_populates='company_openings',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    nomenclature: Final[
        'RelationshipProperty[Optional[CompanyDealAdditionNomenclatureModel]]'
    ] = relationship(
        'CompanyDealAdditionNomenclatureModel',
        back_populates='openings',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    drops: Final[
        'RelationshipProperty[list[ContainerTankCompanyOpeningDropModel]]'
    ] = relationship(
        'ContainerTankCompanyOpeningDropModel',
        back_populates='opening',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )

    __table_args__: Final[Tuple[Union[SchemaItem, Dict[str, Any]]]] = (
        ForeignKeyConstraint(
            [group_owner_id, group_member_id],
            [
                CompanyGroupMemberModel.group_owner_id,
                CompanyGroupMemberModel.person_id,
            ],
            onupdate='CASCADE',
            ondelete='NO ACTION',
        ),
        ForeignKeyConstraint(
            [container_id, tank_type_id],
            [ContainerTankModel.container_id, ContainerTankModel.type_id],
            onupdate='CASCADE',
            ondelete='NO ACTION',
        ),
        ForeignKeyConstraint(
            [addition_id, nomenclature_id],
            [
                CompanyDealAdditionNomenclatureModel.addition_id,
                CompanyDealAdditionNomenclatureModel.nomenclature_id,
            ],
            onupdate='CASCADE',
            ondelete='NO ACTION',
        ),
    )
