from typing import Final

from babel.core import Locale
from sqlalchemy.sql.schema import Column, ForeignKey

from .._mixins import Timestamped
from ..base_interface import Base
from ..locales.locale_model import LocaleModel


class SettingsModel(Timestamped, Base):
    fallback_locale: Final[Column[Locale]] = Column(
        'FallbackLocale',
        LocaleModel.locale.type,
        ForeignKey(
            LocaleModel.locale,
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
        primary_key=True,
        key='fallback_locale',
    )
