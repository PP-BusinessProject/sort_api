from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column
from sqlalchemy.sql.sqltypes import String

from .._mixins import Timestamped
from ..base_interface import Base

if TYPE_CHECKING:
    from .locale_text_model import LocaleTextModel


class TextModel(Timestamped, Base):
    key: Final[Column[str]] = Column(
        'Key',
        String,
        CheckConstraint('"Key" <> \'\''),
        primary_key=True,
        key='key',
    )
    text: Final[Column[str]] = Column(
        'Text',
        String,
        CheckConstraint('"Text" <> \'\''),
        nullable=False,
        key='text',
    )

    locales: Final[
        'RelationshipProperty[list[LocaleTextModel]]'
    ] = relationship(
        'LocaleTextModel',
        back_populates='text',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
