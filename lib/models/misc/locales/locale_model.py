from typing import TYPE_CHECKING, Final, Optional

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column

from ..._mixins import Timestamped
from ..._types import CaseInsensitiveUnicode
from ...base_interface import Base

if TYPE_CHECKING:
    from ...companies.bonuses.categories.company_bonus_category_locale_model import (
        CompanyBonusCategoryLocaleModel,
    )
    from ...companies.bonuses.company_bonus_locale_model import (
        CompanyBonusLocaleModel,
    )
    from ...companies.company_locale_model import CompanyLocaleModel
    from ...companies.contacts.company_contact_locale_model import (
        CompanyContactLocaleModel,
    )
    from ...companies.contacts.types.company_contact_type_locale_model import (
        CompanyContactTypeLocaleModel,
    )
    from ...companies.groups.company_group_locale_model import (
        CompanyGroupLocaleModel,
    )
    from ...companies.groups.rights.company_group_right_locale_model import (
        CompanyGroupRightLocaleModel,
    )
    from ...containers.reports.container_report_type_locale_model import (
        ContainerReportTypeLocaleModel,
    )
    from ...containers.tanks.container_tank_type_locale_model import (
        ContainerTankTypeLocaleModel,
    )
    from ...nomenclatures.categories.nomenclature_category_locale_model import (
        NomenclatureCategoryLocaleModel,
    )
    from ...nomenclatures.nomenclature_locale_model import (
        NomenclatureLocaleModel,
    )
    from ...people.person_locale_model import PersonLocaleModel
    from ..addresses.address_locale_model import AddressLocaleModel
    from ..banks.bank_locale_model import BankLocaleModel
    from ..measurements.measurement_locale_model import MeasurementLocaleModel
    from ..prices.price_locale_model import PriceLocaleModel
    from ..settings_model import SettingsModel
    from .text_locale_model import TextLocaleModel


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
    company_bonus_locales: Final[
        'RelationshipProperty[list[CompanyBonusLocaleModel]]'
    ] = relationship(
        'CompanyBonusLocaleModel',
        back_populates='locale',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    company_bonus_category_locales: Final[
        'RelationshipProperty[list[CompanyBonusCategoryLocaleModel]]'
    ] = relationship(
        'CompanyBonusCategoryLocaleModel',
        back_populates='locale',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    company_locales: Final[
        'RelationshipProperty[list[CompanyLocaleModel]]'
    ] = relationship(
        'CompanyLocaleModel',
        back_populates='locale',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    company_contact_locales: Final[
        'RelationshipProperty[list[CompanyContactLocaleModel]]'
    ] = relationship(
        'CompanyContactLocaleModel',
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
    company_group_locales: Final[
        'RelationshipProperty[list[CompanyGroupLocaleModel]]'
    ] = relationship(
        'CompanyGroupLocaleModel',
        back_populates='locale',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    company_group_right_locales: Final[
        'RelationshipProperty[list[CompanyGroupRightLocaleModel]]'
    ] = relationship(
        'CompanyGroupRightLocaleModel',
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
    measurement_locales: Final[
        'RelationshipProperty[list[MeasurementLocaleModel]]'
    ] = relationship(
        'MeasurementLocaleModel',
        back_populates='locale',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    person_locales: Final[
        'RelationshipProperty[list[PersonLocaleModel]]'
    ] = relationship(
        'PersonLocaleModel',
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
