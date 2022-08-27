from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import String

from ..._mixins import Timestamped
from ...base_interface import Base
from .locale_model import LocaleModel
from .text_model import TextModel


class TextLocaleModel(Timestamped, Base):
    text_key: Final[Column[str]] = Column(
        'TextKey',
        TextModel.key.type,
        ForeignKey(TextModel.key, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
        key='text_key',
    )
    locale_alpha_2: Final[Column[str]] = Column(
        'LocaleAlpha2',
        LocaleModel.alpha_2.type,
        ForeignKey(
            LocaleModel.alpha_2,
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
        primary_key=True,
        key='locale_alpha_2',
    )

    value: Final[Column[str]] = Column(
        'Value',
        String(1023),
        CheckConstraint('"Value" <> \'\''),
        nullable=False,
        key='value',
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
