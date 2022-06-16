from typing import TYPE_CHECKING, Final

from babel.core import Locale
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column
from sqlalchemy_utils.types.locale import LocaleType

from .._mixins import Timestamped
from ..base_interface import Base

if TYPE_CHECKING:
    from .locale_text_model import LocaleTextModel


class LocaleModel(Timestamped, Base):
    locale: Final[Column[Locale]] = Column(
        'Locale',
        LocaleType,
        primary_key=True,
        key='locale',
    )

    texts: Final['RelationshipProperty[list[LocaleTextModel]]'] = relationship(
        'LocaleTextModel',
        back_populates='locale_',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
