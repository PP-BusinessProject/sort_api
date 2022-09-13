from typing import Any, Dict, Final, Tuple, Union

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import (
    CheckConstraint,
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    SchemaItem,
)
from sqlalchemy.sql.sqltypes import String

from ..._mixins import Timestamped
from ...base_interface import Base
from .locale_model import LocaleModel
from .text_model import TextModel


class TextLocaleModel(Timestamped, Base):
    text_key: Final[Column[str]] = Column(
        TextModel.key.type,
        ForeignKey(TextModel.key, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
    )
    locale_language_code: Final[Column[str]] = Column(
        LocaleModel.language_code.type,
        primary_key=True,
    )
    locale_country_code: Final[Column[str]] = Column(
        LocaleModel.country_code.type,
        primary_key=True,
    )

    value: Final[Column[str]] = Column(
        String(1023),
        CheckConstraint("value <> ''"),
        nullable=False,
    )

    locale: Final['RelationshipProperty[LocaleModel]'] = relationship(
        'LocaleModel',
        back_populates='text_locales',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    text: Final['RelationshipProperty[TextModel]'] = relationship(
        'TextModel',
        back_populates='locales',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )

    __table_args__: Final[Tuple[Union[SchemaItem, Dict[str, Any]]]] = (
        ForeignKeyConstraint(
            [locale_language_code, locale_country_code],
            [LocaleModel.language_code, LocaleModel.country_code],
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
    )
