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
from ...misc.locales.locale_model import LocaleModel
from .company_bonus_model import CompanyBonusModel


class CompanyBonusLocaleModel(Timestamped, Base):
    bonus_id: Final[Column[str]] = Column(
        CompanyBonusModel.id.type,
        ForeignKey(
            CompanyBonusModel.id, onupdate='CASCADE', ondelete='CASCADE',
        ),
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

    name: Final[Column[str]] = Column(
        String(255),
        CheckConstraint("name <> ''"),
        nullable=False,
    )
    description: Final[Column[str]] = Column(
        String(1023),
        nullable=False,
        default='',
    )

    locale: Final['RelationshipProperty[LocaleModel]'] = relationship(
        'LocaleModel',
        back_populates='company_bonus_locales',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    bonus: Final['RelationshipProperty[CompanyBonusModel]'] = relationship(
        'CompanyBonusModel',
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
