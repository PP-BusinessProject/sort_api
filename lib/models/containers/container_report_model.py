from typing import Any, Dict, Final, Optional, Tuple, Union

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import (
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    SchemaItem,
)
from sqlalchemy.sql.sqltypes import Integer, String

from .._mixins import Timestamped
from ..base_interface import Base
from ..clients.user_model import UserModel
from .container_model import ContainerModel
from .container_report_type_model import ContainerReportTypeModel
from .container_tank_model import ContainerTankModel


class ContainerReportModel(Timestamped, Base):
    user_id: Final[Column[Optional[int]]] = Column(
        'UserId',
        UserModel.id.type,
        ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='NO ACTION'),
        nullable=False,
        key='user_id',
    )
    container_id: Final[Column[int]] = Column(
        'ContainerId',
        ContainerModel.id.type,
        ForeignKey(ContainerModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        key='container_id',
    )
    # type_id: Final[Column[Optional[int]]] = Column(
    #     'TypeId',
    #     ContainerTankModel.type_id.type,
    #     nullable=False,
    #     key='type_id',
    # )

    id: Final[Column[int]] = Column(
        'Id',
        Integer,
        primary_key=True,
        autoincrement=True,
        key='id',
    )
    type: Final[Column[int]] = Column(
        'Type',
        ContainerReportTypeModel.id.type,
        ForeignKey(
            ContainerReportTypeModel.id,
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        nullable=False,
        key='type',
    )
    information: Final[Column[str]] = Column(
        'Information',
        String(1023),
        nullable=False,
        default='',
        key='information',
    )

    type_: Final[
        'RelationshipProperty[ContainerReportTypeModel]'
    ] = relationship(
        'ContainerReportTypeModel',
        back_populates='reports',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    container: Final['RelationshipProperty[ContainerModel]'] = relationship(
        'ContainerModel',
        back_populates='reports',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )

    # __table_args__: Final[Tuple[Union[SchemaItem, Dict[str, Any]]]] = (
    #     ForeignKeyConstraint(
    #         [container_id, type_id],
    #         [ContainerTankModel.container_id, ContainerTankModel.type_id],
    #         onupdate='CASCADE',
    #         ondelete='NO ACTION',
    #     ),
    # )
