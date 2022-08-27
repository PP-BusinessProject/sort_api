from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column

from ..._mixins import Timestamped
from ..._types import CaseInsensitiveUnicode
from ...base_interface import Base

if TYPE_CHECKING:
    from ...bonuses.bonus_locale_model import BonusLocaleModel
    from ...clients.companies.company_contact_type_locale_model import (
        CompanyContactTypeLocaleModel,
    )
    from ...clients.groups.group_right_locale_model import (
        GroupRightLocaleModel,
    )
    from ...clients.services.service_locale_model import ServiceLocaleModel
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


class LocaleModel(Timestamped, Base):
    alpha_2: Final[Column[str]] = Column(
        'Alpha2',
        CaseInsensitiveUnicode(2),
        primary_key=True,
        key='alpha_2',
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
    service_locales: Final[
        'RelationshipProperty[list[ServiceLocaleModel]]'
    ] = relationship(
        'ServiceLocaleModel',
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
    user_locales: Final[
        'RelationshipProperty[list[UserLocaleModel]]'
    ] = relationship(
        'UserLocaleModel',
        back_populates='locale',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
