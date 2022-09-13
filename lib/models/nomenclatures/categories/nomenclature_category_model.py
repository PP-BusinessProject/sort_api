from typing import TYPE_CHECKING, Final, Optional

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from typing_extensions import Self

from ...base_interface import Base

if TYPE_CHECKING:
    from ..nomenclature_model import NomenclatureModel
    from .nomenclature_category_locale_model import (
        NomenclatureCategoryLocaleModel,
    )


class NomenclatureCategoryModel(Base):
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
        'RelationshipProperty[list[NomenclatureCategoryLocaleModel]]'
    ] = relationship(
        'NomenclatureCategoryLocaleModel',
        back_populates='category',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    parent: Final['RelationshipProperty[Optional[Self]]'] = relationship(
        'NomenclatureCategoryModel',
        back_populates='children',
        lazy='noload',
        cascade='save-update',
        remote_side=[id],
        uselist=False,
    )
    children: Final['RelationshipProperty[list[Self]]'] = relationship(
        'NomenclatureCategoryModel',
        back_populates='parent',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    nomenclatures: Final[
        'RelationshipProperty[list[NomenclatureModel]]'
    ] = relationship(
        'NomenclatureModel',
        back_populates='category',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
