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

from ...base_interface import Base
from ..locales.locale_model import LocaleModel
from .address_model import AddressModel


class AddressLocaleModel(Base):
    address_id: Final[Column[int]] = Column(
        'AddressId',
        ForeignKey(
            AddressModel.id,
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        primary_key=True,
        autoincrement=True,
        key='address_id',
    )
    locale_language_code: Final[Column[str]] = Column(
        'LocaleLanguageCode',
        LocaleModel.language_code.type,
        primary_key=True,
        key='locale_language_code',
    )
    locale_country_code: Final[Column[str]] = Column(
        'LocaleCountryCode',
        LocaleModel.country_code.type,
        primary_key=True,
        key='locale_country_code',
    )

    country: Final[Column[str]] = Column(
        'Сountry',
        String(255),
        CheckConstraint('"Сountry" <> \'\''),
        nullable=False,
        default='Ukraine',
        key='country',
    )
    state: Final[Column[str]] = Column(
        'State',
        String(255),
        CheckConstraint('"State" <> \'\''),
        nullable=False,
        key='state',
    )
    city: Final[Column[str]] = Column(
        'City',
        String(255),
        CheckConstraint('"City" <> \'\''),
        nullable=False,
        key='city',
    )
    street: Final[Column[str]] = Column(
        'Street',
        String(255),
        CheckConstraint('"Street" <> \'\''),
        nullable=False,
        key='street',
    )

    locale: Final['RelationshipProperty[LocaleModel]'] = relationship(
        'LocaleModel',
        back_populates='address_locales',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    address: Final['RelationshipProperty[AddressModel]'] = relationship(
        'AddressModel',
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
