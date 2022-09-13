from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column
from sqlalchemy.sql.sqltypes import Integer, String

from ..._mixins import Timestamped
from ...base_interface import Base

if TYPE_CHECKING:
    from ..tanks.container_tank_type_locale_model import (
        ContainerReportTypeLocaleModel,
    )
    from .container_report_model import ContainerReportModel


class ContainerReportTypeModel(Timestamped, Base):
    id: Final[Column[int]] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    fallback_name: Final[Column[str]] = Column(
        String(255),
        CheckConstraint("fallback_name <> ''"),
        nullable=False,
    )

    locales: Final[
        'RelationshipProperty[list[ContainerReportTypeLocaleModel]]'
    ] = relationship(
        'ContainerReportTypeLocaleModel',
        back_populates='type',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    reports: Final[
        'RelationshipProperty[list[ContainerReportModel]]'
    ] = relationship(
        'ContainerReportModel',
        back_populates='type',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
