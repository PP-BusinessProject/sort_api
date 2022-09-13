from typing import TYPE_CHECKING, Final, Optional

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from typing_extensions import Self

from ...base_interface import Base

if TYPE_CHECKING:
    from ..bonus_model import BonusModel
    from .bonus_category_locale_model import BonusCategoryLocaleModel


class BonusCategoryModel(Base):
    id: Final[Column[int]] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    parent_id: Final[Column[Optional[int]]] = Column(
        id.type,
        ForeignKey(id, onupdate='CASCADE', ondelete='CASCADE'),
        CheckConstraint('parent_id <> "Id"'),
    )

    fallback_name: Final[Column[str]] = Column(
        String(255),
        CheckConstraint("fallback_name <> ''"),
        nullable=False,
    )

    locales: Final[
        'RelationshipProperty[list[BonusCategoryLocaleModel]]'
    ] = relationship(
        'BonusCategoryLocaleModel',
        back_populates='category',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    parent: Final['RelationshipProperty[Optional[Self]]'] = relationship(
        'BonusCategoryModel',
        back_populates='children',
        lazy='noload',
        cascade='save-update',
        remote_side=[id],
        uselist=False,
    )
    children: Final['RelationshipProperty[list[Self]]'] = relationship(
        'BonusCategoryModel',
        back_populates='parent',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    bonuses: Final['RelationshipProperty[list[BonusModel]]'] = relationship(
        'BonusModel',
        back_populates='category',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
