from typing import Final, Literal

from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean

from .._mixins import Timestamped
from ..base_interface import Base
from .locales.locale_model import LocaleModel


class SettingsModel(Timestamped, Base):
    __tablename__: Final[str] = 'Settings'

    id: Final[Column[Literal[True]]] = Column(
        'Id',
        Boolean(create_constraint=True),
        CheckConstraint('"Id"'),
        primary_key=True,
        default=True,
        key='id',
    )
    fallback_locale_alpha_2: Final[Column[str]] = Column(
        'FallbackLocaleAlpha2',
        LocaleModel.alpha_2.type,
        ForeignKey(
            LocaleModel.alpha_2,
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
        nullable=False,
        default='uk',
        key='fallback_locale_alpha_2',
    )
