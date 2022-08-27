from typing import Final, Optional

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from ..._mixins import Timestamped
from ...base_interface import Base
from ...clients.user_model import UserModel
from ..container_model import ContainerModel
from .container_report_type_model import ContainerReportTypeModel


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

    id: Final[Column[int]] = Column(
        'Id',
        Integer,
        primary_key=True,
        autoincrement=True,
        key='id',
    )
    type_id: Final[Column[int]] = Column(
        'TypeId',
        ContainerReportTypeModel.id.type,
        ForeignKey(
            ContainerReportTypeModel.id,
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        nullable=False,
        key='type_id',
    )
    information: Final[Column[str]] = Column(
        'Information',
        String(1023),
        nullable=False,
        default='',
        key='information',
    )

    type: Final[
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
