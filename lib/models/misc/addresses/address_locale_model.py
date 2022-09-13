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
        ForeignKey(
            AddressModel.id,
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        primary_key=True,
        autoincrement=True,
    )
    locale_language_code: Final[Column[str]] = Column(
        LocaleModel.language_code.type,
        primary_key=True,
    )
    locale_country_code: Final[Column[str]] = Column(
        LocaleModel.country_code.type,
        primary_key=True,
    )

    country: Final[Column[str]] = Column(
        String(255),
        CheckConstraint("country <> ''"),
        nullable=False,
        default='Ukraine',
    )
    state: Final[Column[str]] = Column(
        String(255),
        CheckConstraint("state <> ''"),
        nullable=False,
    )
    city: Final[Column[str]] = Column(
        String(255),
        CheckConstraint("city <> ''"),
        nullable=False,
    )
    street: Final[Column[str]] = Column(
        String(255),
        CheckConstraint("street <> ''"),
        nullable=False,
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
