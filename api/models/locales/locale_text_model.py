from typing import Final

from babel.core import Locale
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
    locale: Final[Column[Locale]] = Column(
        'Locale',
        LocaleModel.locale.type,
        ForeignKey(
            LocaleModel.locale,
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
        primary_key=True,
        key='locale',
    )
    text: Final[Column[str]] = Column(
        'Text',
        String,
        CheckConstraint('"Text" <> \'\''),
        nullable=False,
        key='text',
    )

    locale_: Final['RelationshipProperty[LocaleModel]'] = relationship(
        'LocaleModel',
        back_populates='texts',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    text_: Final['RelationshipProperty[TextModel]'] = relationship(
        'TextModel',
        back_populates='locales',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
