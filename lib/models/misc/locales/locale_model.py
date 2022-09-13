from typing import TYPE_CHECKING, Final, Optional

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, CheckConstraint

from ..._mixins import Timestamped
from ..._types import CaseInsensitiveUnicode
from ...base_interface import Base

if TYPE_CHECKING:
    from ...bonuses.bonus_locale_model import BonusLocaleModel
    from ...bonuses.categories.bonus_category_locale_model import (
        BonusCategoryLocaleModel,
    )
    from ...clients.companies.company_contact_type_locale_model import (
        CompanyContactTypeLocaleModel,
    )
    from ...clients.groups.group_right_locale_model import (
        GroupRightLocaleModel,
    )
    from ...nomenclatures.nomenclature_locale_model import (
        NomenclatureLocaleModel,
    )
    from ...nomenclatures.categories.nomenclature_category_locale_model import (
        NomenclatureCategoryLocaleModel,
    )
    from ...containers.reports.container_report_type_locale_model import (
        ContainerReportTypeLocaleModel,
    )
    from ...containers.tanks.container_tank_type_locale_model import (
        ContainerTankTypeLocaleModel,
    )
    from ..measurements.measurement_locale_model import (
        MeasurementLocaleModel,
    )
    from ..prices.price_locale_model import PriceLocaleModel
    from ..addresses.address_locale_model import AddressLocaleModel
    from ..banks.bank_locale_model import BankLocaleModel
    from .text_locale_model import TextLocaleModel
    from ...clients.user_locale_model import UserLocaleModel
    from ..settings_model import SettingsModel


class LocaleModel(Timestamped, Base):
    language_code: Final[Column[str]] = Column(
        CaseInsensitiveUnicode(2),
        CheckConstraint("language_code <> ''"),
        primary_key=True,
    )
    country_code: Final[Column[str]] = Column(
        CaseInsensitiveUnicode(2),
        CheckConstraint("country_code <> ''"),
        primary_key=True,
    )

    settings: Final[
        'RelationshipProperty[Optional[SettingsModel]]'
    ] = relationship(
        'SettingsModel',
        back_populates='fallback_locale',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    address_locales: Final[
        'RelationshipProperty[list[AddressLocaleModel]]'
    ] = relationship(
        'AddressLocaleModel',
        back_populates='locale',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    bank_locales: Final[
        'RelationshipProperty[list[BankLocaleModel]]'
    ] = relationship(
        'BankLocaleModel',
        back_populates='locale',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    bonus_locales: Final[
        'RelationshipProperty[list[BonusLocaleModel]]'
    ] = relationship(
        'BonusLocaleModel',
        back_populates='locale',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    bonus_category_locales: Final[
        'RelationshipProperty[list[BonusCategoryLocaleModel]]'
    ] = relationship(
        'BonusCategoryLocaleModel',
        back_populates='locale',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    company_contact_type_locales: Final[
        'RelationshipProperty[list[CompanyContactTypeLocaleModel]]'
    ] = relationship(
        'CompanyContactTypeLocaleModel',
        back_populates='locale',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    container_report_type_locales: Final[
        'RelationshipProperty[list[ContainerReportTypeLocaleModel]]'
    ] = relationship(
        'ContainerReportTypeLocaleModel',
        back_populates='locale',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    container_tank_type_locales: Final[
        'RelationshipProperty[list[ContainerTankTypeLocaleModel]]'
    ] = relationship(
        'ContainerTankTypeLocaleModel',
        back_populates='locale',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    group_right_locales: Final[
        'RelationshipProperty[list[GroupRightLocaleModel]]'
    ] = relationship(
        'GroupRightLocaleModel',
        back_populates='locale',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    measurement_locales: Final[
        'RelationshipProperty[list[MeasurementLocaleModel]]'
    ] = relationship(
        'MeasurementLocaleModel',
        back_populates='locale',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    price_locales: Final[
        'RelationshipProperty[list[PriceLocaleModel]]'
    ] = relationship(
        'PriceLocaleModel',
        back_populates='locale',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    text_locales: Final[
        'RelationshipProperty[list[TextLocaleModel]]'
    ] = relationship(
        'TextLocaleModel',
        back_populates='locale',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    nomenclature_category_locales: Final[
        'RelationshipProperty[list[NomenclatureCategoryLocaleModel]]'
    ] = relationship(
        'NomenclatureCategoryLocaleModel',
        back_populates='locale',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    nomenclature_locales: Final[
        'RelationshipProperty[list[NomenclatureLocaleModel]]'
    ] = relationship(
        'NomenclatureLocaleModel',
        back_populates='locale',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    user_locales: Final[
        'RelationshipProperty[list[UserLocaleModel]]'
    ] = relationship(
        'UserLocaleModel',
        back_populates='locale',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
