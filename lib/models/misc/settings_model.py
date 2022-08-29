from typing import Any, Dict, Final, Literal, Optional, Tuple, Union

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import (
    CheckConstraint,
    Column,
    ForeignKeyConstraint,
    SchemaItem,
)
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

    fallback_locale_language_code: Final[Column[Optional[str]]] = Column(
        'FallbackLocaleLanguageCode',
        LocaleModel.language_code.type,
        key='fallback_locale_language_code',
    )
    fallback_locale_country_code: Final[Column[Optional[str]]] = Column(
        'FallbackLocaleCountryCode',
        LocaleModel.country_code.type,
        key='fallback_locale_country_code',
    )

    fallback_locale: Final[
        'RelationshipProperty[Optional[LocaleModel]]'
    ] = relationship(
        'LocaleModel',
        back_populates='settings',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )

    __table_args__: Final[Tuple[Union[SchemaItem, Dict[str, Any]]]] = (
        ForeignKeyConstraint(
            [fallback_locale_language_code, fallback_locale_country_code],
            [LocaleModel.language_code, LocaleModel.country_code],
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
    )
