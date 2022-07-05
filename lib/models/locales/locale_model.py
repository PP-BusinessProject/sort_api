from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column

from .._mixins import Timestamped
from .._types import CaseInsensitiveUnicode
from ..base_interface import Base

if TYPE_CHECKING:
    from .locale_text_model import LocaleTextModel


class LocaleModel(Timestamped, Base):
    locale_alpha_2: Final[Column[str]] = Column(
        'LocaleAlpha2',
        CaseInsensitiveUnicode(2),
        primary_key=True,
        key='locale_alpha_2',
    )

    texts: Final['RelationshipProperty[list[LocaleTextModel]]'] = relationship(
        'LocaleTextModel',
        back_populates='locale',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
