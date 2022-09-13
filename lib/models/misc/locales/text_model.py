from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column
from sqlalchemy.sql.sqltypes import String

from ..._mixins import Timestamped
from ...base_interface import Base

if TYPE_CHECKING:
    from .text_locale_model import TextLocaleModel


class TextModel(Timestamped, Base):
    key: Final[Column[str]] = Column(
        String(255),
        CheckConstraint("key <> ''"),
        primary_key=True,
    )
    fallback: Final[Column[str]] = Column(
        String(1023),
        CheckConstraint("fallback <> ''"),
        nullable=False,
    )

    locales: Final[
        'RelationshipProperty[list[TextLocaleModel]]'
    ] = relationship(
        'TextLocaleModel',
        back_populates='text',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
