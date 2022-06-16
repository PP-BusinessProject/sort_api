from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer

from .._mixins import Timestamped
from ..base_interface import Base

if TYPE_CHECKING:
    from .container_report_model import ContainerReportModel


class ContainerReportTypeModel(Timestamped, Base):
    id: Final[Column[int]] = Column(
        'Id',
        Integer,
        primary_key=True,
        autoincrement=True,
        key='id',
    )

    reports: Final[
        'RelationshipProperty[list[ContainerReportModel]]'
    ] = relationship(
        'ContainerReportModel',
        back_populates='type_',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
