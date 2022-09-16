"""The module that provides a `GroupModel`."""


from typing import TYPE_CHECKING, Final
from uuid import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import String

from ..._mixins import Timestamped
from ...base_interface import Base
from ..company_model import CompanyModel

if TYPE_CHECKING:
    from .company_group_locale_model import CompanyGroupLocaleModel
    from .members.company_group_member_model import CompanyGroupMemberModel


class CompanyGroupModel(Timestamped, Base):

    owner_id: Final[Column[UUID]] = Column(
        CompanyModel.user_id.type,
        ForeignKey(
            CompanyModel.user_id, onupdate='CASCADE', ondelete='CASCADE'
        ),
        primary_key=True,
    )
    fallback_name: Final[Column[str]] = Column(
        String(64),
        nullable=False,
        default='',
    )

    locales: Final[
        'RelationshipProperty[list[CompanyGroupLocaleModel]]'
    ] = relationship(
        'CompanyGroupLocaleModel',
        back_populates='group',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    owner: Final['RelationshipProperty[CompanyModel]'] = relationship(
        'CompanyModel',
        back_populates='group',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    members: Final[
        'RelationshipProperty[list[CompanyGroupMemberModel]]'
    ] = relationship(
        'CompanyGroupMemberModel',
        back_populates='group',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
