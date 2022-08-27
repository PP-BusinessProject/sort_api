from typing import TYPE_CHECKING, Any, Dict, Final, Tuple, Type, Union

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

from ...._mixins import Timestamped
from ....base_interface import Base
from ....clients.deals.deal_service_model import DealServiceModel
from ....clients.user_model import UserModel
from ..container_tank_model import ContainerTankModel

if TYPE_CHECKING:
    from .container_tank_opening_drop_model import (
        ContainerTankOpeningDropModel,
    )


class ContainerTankOpeningModel(Timestamped, Base):
    user_id: Final[Column[int]] = Column(
        'UserId',
        UserModel.id.type,
        ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='NO ACTION'),
        nullable=False,
        key='user_id',
    )
    container_id: Final[Column[int]] = Column(
        'ContainerId',
        ContainerTankModel.container_id.type,
        nullable=False,
        key='container_id',
    )
    tank_type_id: Final[Column[int]] = Column(
        'TankTypeId',
        ContainerTankModel.type_id.type,
        nullable=False,
        key='tank_type_id',
    )
    deal_id: Final[Column[int]] = Column(
        'DealId',
        DealServiceModel.deal_id.type,
        nullable=False,
        key='deal_id',
    )
    service_id: Final[Column[int]] = Column(
        'ServiceId',
        DealServiceModel.service_id.type,
        nullable=False,
        key='service_id',
    )

    id: Final[Column[int]] = Column(
        'Id',
        Integer,
        primary_key=True,
        autoincrement=True,
        key='id',
    )

    @hybrid_property
    def volume(self: Self, /) -> int:  # noqa: D102
        return sum(drop.volume for drop in self.drops)

    @volume.expression
    def volume(cls: Type[Self], /) -> ClauseElement:
        return func.sum(ContainerTankOpeningDropModel.volume).select_from(
            cls.drops
        )

    user: Final['RelationshipProperty[UserModel]'] = relationship(
        'UserModel',
        back_populates='openings',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    tank: Final['RelationshipProperty[ContainerTankModel]'] = relationship(
        'ContainerTankModel',
        back_populates='openings',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    deal_service: Final[
        'RelationshipProperty[DealServiceModel]'
    ] = relationship(
        'DealServiceModel',
        back_populates='openings',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    drops: Final[
        'RelationshipProperty[list[ContainerTankOpeningDropModel]]'
    ] = relationship(
        'ContainerTankOpeningDropModel',
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
            [deal_id, service_id],
            [DealServiceModel.deal_id, DealServiceModel.service_id],
            onupdate='CASCADE',
            ondelete='NO ACTION',
        ),
    )
