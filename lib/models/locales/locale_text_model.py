from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import String

from .._mixins import Timestamped
from ..base_interface import Base
from .locale_model import LocaleModel
from .text_model import TextModel


class LocaleTextModel(Timestamped, Base):
    key: Final[Column[str]] = Column(
        'Key',
        TextModel.key.type,
        ForeignKey(TextModel.key, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
        key='key',
    )
    locale_alpha_2: Final[Column[str]] = Column(
        'LocaleAlpha2',
        LocaleModel.locale_alpha_2.type,
        ForeignKey(
            LocaleModel.locale_alpha_2,
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
        primary_key=True,
        key='locale_alpha_2',
    )
    fallback_text: Final[Column[str]] = Column(
        'FallbackText',
        String,
        CheckConstraint('"FallbackText" <> \'\''),
        nullable=False,
        key='fallback_text',
    )

    locale: Final['RelationshipProperty[LocaleModel]'] = relationship(
        'LocaleModel',
        back_populates='texts',
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
