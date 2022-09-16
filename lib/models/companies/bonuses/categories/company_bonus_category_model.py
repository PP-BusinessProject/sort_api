from typing import TYPE_CHECKING, Final, Optional

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from typing_extensions import Self

from ....base_interface import Base

if TYPE_CHECKING:
    from ..company_bonus_model import CompanyBonusModel
    from .company_bonus_category_locale_model import (
        CompanyBonusCategoryLocaleModel,
    )


class CompanyBonusCategoryModel(Base):
    id: Final[Column[int]] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    parent_id: Final[Column[Optional[int]]] = Column(
        id.type,
        ForeignKey(id, onupdate='CASCADE', ondelete='CASCADE'),
        CheckConstraint('parent_id <> id'),
    )

    fallback_name: Final[Column[str]] = Column(
        String(255),
        CheckConstraint("fallback_name <> ''"),
        nullable=False,
    )

    locales: Final[
        'RelationshipProperty[list[CompanyBonusCategoryLocaleModel]]'
    ] = relationship(
        'CompanyBonusCategoryLocaleModel',
        back_populates='category',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    parent: Final['RelationshipProperty[Optional[Self]]'] = relationship(
        'CompanyBonusCategoryModel',
        back_populates='children',
        lazy='noload',
        cascade='save-update',
        remote_side=[id],
        uselist=False,
    )
    children: Final['RelationshipProperty[list[Self]]'] = relationship(
        'CompanyBonusCategoryModel',
        back_populates='parent',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    bonuses: Final[
        'RelationshipProperty[list[CompanyBonusModel]]'
    ] = relationship(
        'CompanyBonusModel',
        back_populates='category',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
