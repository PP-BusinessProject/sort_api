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
from .container_report_type_model import ContainerReportTypeModel


class ContainerReportTypeLocaleModel(Timestamped, Base):
    type_id: Final[Column[int]] = Column(
        'TypeId',
        ContainerReportTypeModel.id.type,
        ForeignKey(
            ContainerReportTypeModel.id,
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        primary_key=True,
        key='type_id',
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

    name: Final[Column[str]] = Column(
        'Name',
        String(255),
        CheckConstraint('"Name" <> \'\''),
        nullable=False,
        key='name',
    )

    locale: Final['RelationshipProperty[LocaleModel]'] = relationship(
        'LocaleModel',
        back_populates='container_report_type_locales',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    type: Final[
        'RelationshipProperty[ContainerReportTypeModel]'
    ] = relationship(
        'ContainerReportTypeModel',
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
