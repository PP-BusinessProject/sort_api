from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column
from sqlalchemy.sql.sqltypes import Integer, String

from ...._mixins import Timestamped
from ....base_interface import Base

if TYPE_CHECKING:
    from ..members.company_group_member_right_model import (
        CompanyGroupMemberRightModel,
    )
    from .company_group_right_locale_model import CompanyGroupRightLocaleModel


class CompanyGroupRightModel(Timestamped, Base):
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
        'RelationshipProperty[list[CompanyGroupRightLocaleModel]]'
    ] = relationship(
        'CompanyGroupRightLocaleModel',
        back_populates='right',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    members: Final[
        'RelationshipProperty[list[CompanyGroupMemberRightModel]]'
    ] = relationship(
        'CompanyGroupMemberRightModel',
        back_populates='right',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
