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

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.elements import ClauseElement
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import (
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    SchemaItem,
)
from sqlalchemy.sql.sqltypes import Integer
from typing_extensions import Self

from ....._mixins import Timestamped
from .....base_interface import Base
from .....people.deals.additions.person_deal_addition_nomenclature_model import (
    PersonDealAdditionNomenclatureModel,
)
from .....people.person_model import PersonModel
from ...container_tank_model import ContainerTankModel

if TYPE_CHECKING:
    from .container_tank_person_opening_drop_model import (
        ContainerTankPersonOpeningDropModel,
    )


class ContainerTankPersonOpeningModel(Timestamped, Base):
    person_id: Final[Column[int]] = Column(
        PersonModel.user_id.type,
        ForeignKey(
            PersonModel.user_id, onupdate='CASCADE', ondelete='NO ACTION'
        ),
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
        PersonDealAdditionNomenclatureModel.addition_id.type,
        nullable=False,
    )
    nomenclature_id: Final[Column[int]] = Column(
        PersonDealAdditionNomenclatureModel.nomenclature_id.type,
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
            ContainerTankPersonOpeningDropModel.volume
        ).select_from(cls.drops)

    person: Final['RelationshipProperty[PersonModel]'] = relationship(
        'PersonModel',
        back_populates='openings',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    tank: Final['RelationshipProperty[ContainerTankModel]'] = relationship(
        'ContainerTankModel',
        back_populates='person_openings',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    nomenclature: Final[
        'RelationshipProperty[Optional[PersonDealAdditionNomenclatureModel]]'
    ] = relationship(
        'PersonDealAdditionNomenclatureModel',
        back_populates='openings',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    drops: Final[
        'RelationshipProperty[list[ContainerTankPersonOpeningDropModel]]'
    ] = relationship(
        'ContainerTankPersonOpeningDropModel',
        back_populates='opening',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )

    __table_args__: Final[Tuple[Union[SchemaItem, Dict[str, Any]]]] = (
        ForeignKeyConstraint(
            [container_id, tank_type_id],
            [ContainerTankModel.container_id, ContainerTankModel.type_id],
            onupdate='CASCADE',
            ondelete='NO ACTION',
        ),
        ForeignKeyConstraint(
            [addition_id, nomenclature_id],
            [
                PersonDealAdditionNomenclatureModel.addition_id,
                PersonDealAdditionNomenclatureModel.nomenclature_id,
            ],
            onupdate='CASCADE',
            ondelete='NO ACTION',
        ),
    )
