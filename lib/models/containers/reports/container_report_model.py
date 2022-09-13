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
        UserModel.id.type,
        ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='NO ACTION'),
        nullable=False,
    )
    container_id: Final[Column[int]] = Column(
        ContainerModel.id.type,
        ForeignKey(ContainerModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
    )

    id: Final[Column[int]] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    type_id: Final[Column[int]] = Column(
        ContainerReportTypeModel.id.type,
        ForeignKey(
            ContainerReportTypeModel.id,
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
    )
    information: Final[Column[str]] = Column(
        String(1023),
        nullable=False,
        default='',
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
