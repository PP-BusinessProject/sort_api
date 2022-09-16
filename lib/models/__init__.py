from typing import Final, Tuple

from ._mixins import Timestamped
from .auth.audit_log_entry_model import AuditLogEntryModel
from .auth.identity_model import IdentityModel
from .auth.instance_model import InstanceModel
from .auth.refresh_token_model import RefreshTokenModel
from .auth.schema_migration_model import SchemaMigrationModel
from .auth.session_model import SessionModel
from .auth.user_model import UserModel
from .base_interface import BaseInterface
from .companies.bonuses.categories.company_bonus_category_locale_model import (
    CompanyBonusCategoryLocaleModel,
)
from .companies.bonuses.categories.company_bonus_category_model import (
    CompanyBonusCategoryModel,
)
from .companies.bonuses.company_bonus_image_model import CompanyBonusImageModel
from .companies.bonuses.company_bonus_locale_model import (
    CompanyBonusLocaleModel,
)
from .companies.bonuses.company_bonus_model import CompanyBonusModel
from .companies.bonuses.company_bonus_price_model import CompanyBonusPriceModel
from .companies.bonuses.coupons.company_bonus_coupon_model import (
    CompanyBonusCouponModel,
)
from .companies.bonuses.coupons.company_bonus_coupon_use_model import (
    CompanyBonusCouponUseModel,
)
from .companies.company_image_model import CompanyImageModel
from .companies.company_locale_model import CompanyLocaleModel
from .companies.company_model import CompanyModel
from .companies.contacts.company_contact_locale_model import (
    CompanyContactLocaleModel,
)
from .companies.contacts.company_contact_model import CompanyContactModel
from .companies.contacts.types.company_contact_type_locale_model import (
    CompanyContactTypeLocaleModel,
)
from .companies.contacts.types.company_contact_type_model import (
    CompanyContactTypeModel,
)
from .companies.deals.additions.company_deal_addition_model import (
    CompanyDealAdditionModel,
)
from .companies.deals.additions.company_deal_addition_nomenclature_model import (
    CompanyDealAdditionNomenclatureModel,
)
from .companies.deals.company_deal_model import CompanyDealModel
from .companies.groups.company_group_locale_model import (
    CompanyGroupLocaleModel,
)
from .companies.groups.company_group_model import CompanyGroupModel
from .companies.groups.members.company_group_member_model import (
    CompanyGroupMemberModel,
)
from .companies.groups.members.company_group_member_right_model import (
    CompanyGroupMemberRightModel,
)
from .companies.groups.rights.company_group_right_locale_model import (
    CompanyGroupRightLocaleModel,
)
from .companies.groups.rights.company_group_right_model import (
    CompanyGroupRightModel,
)
from .containers.container_image_model import ContainerImageModel
from .containers.container_model import ContainerModel
from .containers.reports.container_report_model import ContainerReportModel
from .containers.reports.container_report_type_locale_model import (
    ContainerReportTypeLocaleModel,
)
from .containers.reports.container_report_type_model import (
    ContainerReportTypeModel,
)
from .containers.tanks.container_tank_model import ContainerTankModel
from .containers.tanks.container_tank_type_locale_model import (
    ContainerTankTypeLocaleModel,
)
from .containers.tanks.container_tank_type_model import ContainerTankTypeModel

# from .containers.tanks.operations.container_tank_clearing_model import (
#     ContainerTankClearingModel,
# )
from .containers.tanks.operations.openings.container_tank_company_opening_drop_model import (
    ContainerTankCompanyOpeningDropModel,
)
from .containers.tanks.operations.openings.container_tank_company_opening_model import (
    ContainerTankCompanyOpeningModel,
)
from .containers.tanks.operations.openings.container_tank_person_opening_drop_model import (
    ContainerTankPersonOpeningDropModel,
)
from .containers.tanks.operations.openings.container_tank_person_opening_model import (
    ContainerTankPersonOpeningModel,
)

# from .deliveries.delivery_model import DeliveryModel
# from .deliveries.delivery_nomenclature_model import DeliveryNomenclatureModel
from .misc.addresses.address_locale_model import AddressLocaleModel
from .misc.addresses.address_model import AddressModel
from .misc.banks.bank_locale_model import BankLocaleModel
from .misc.banks.bank_model import BankModel
from .misc.image_model import ImageModel
from .misc.locales.locale_model import LocaleModel
from .misc.locales.text_locale_model import TextLocaleModel
from .misc.locales.text_model import TextModel
from .misc.measurements.measurement_locale_model import MeasurementLocaleModel
from .misc.measurements.measurement_model import MeasurementModel
from .misc.prices.price_locale_model import PriceLocaleModel
from .misc.prices.price_model import PriceModel
from .misc.settings_model import SettingsModel
from .nomenclatures.categories.nomenclature_category_locale_model import (
    NomenclatureCategoryLocaleModel,
)
from .nomenclatures.categories.nomenclature_category_model import (
    NomenclatureCategoryModel,
)
from .nomenclatures.nomenclature_image_model import NomenclatureImageModel
from .nomenclatures.nomenclature_locale_model import NomenclatureLocaleModel
from .nomenclatures.nomenclature_model import NomenclatureModel
from .nomenclatures.nomenclature_price_model import NomenclaturePriceModel
from .people.deals.additions.person_deal_addition_model import (
    PersonDealAdditionModel,
)
from .people.deals.additions.person_deal_addition_nomenclature_model import (
    PersonDealAdditionNomenclatureModel,
)
from .people.deals.person_deal_model import PersonDealModel
from .people.person_image_model import PersonImageModel
from .people.person_locale_model import PersonLocaleModel
from .people.person_model import PersonModel

__all__: Final[Tuple[str, ...]] = (
    'Timestamped',
    'AuditLogEntryModel',
    'IdentityModel',
    'InstanceModel',
    'RefreshTokenModel',
    'SchemaMigrationModel',
    'SessionModel',
    'UserModel',
    'BaseInterface',
    'CompanyBonusCategoryLocaleModel',
    'CompanyBonusCategoryModel',
    'CompanyBonusImageModel',
    'CompanyBonusLocaleModel',
    'CompanyBonusModel',
    'CompanyBonusPriceModel',
    'CompanyBonusCouponModel',
    'CompanyBonusCouponUseModel',
    'CompanyImageModel',
    'CompanyLocaleModel',
    'CompanyModel',
    'CompanyContactLocaleModel',
    'CompanyContactModel',
    'CompanyContactTypeLocaleModel',
    'CompanyContactTypeModel',
    'CompanyDealAdditionModel',
    'CompanyDealAdditionNomenclatureModel',
    'CompanyDealModel',
    'CompanyGroupLocaleModel',
    'CompanyGroupModel',
    'CompanyGroupMemberModel',
    'CompanyGroupMemberRightModel',
    'CompanyGroupRightLocaleModel',
    'CompanyGroupRightModel',
    'ContainerImageModel',
    'ContainerModel',
    'ContainerReportModel',
    'ContainerReportTypeLocaleModel',
    'ContainerReportTypeModel',
    'ContainerTankModel',
    'ContainerTankTypeLocaleModel',
    'ContainerTankTypeModel',
    # 'ContainerTankClearingModel',
    'ContainerTankCompanyOpeningDropModel',
    'ContainerTankCompanyOpeningModel',
    'ContainerTankPersonOpeningDropModel',
    'ContainerTankPersonOpeningModel',
    # 'DeliveryModel',
    # 'DeliveryNomenclatureModel',
    'AddressLocaleModel',
    'AddressModel',
    'BankLocaleModel',
    'BankModel',
    'ImageModel',
    'LocaleModel',
    'TextLocaleModel',
    'TextModel',
    'MeasurementLocaleModel',
    'MeasurementModel',
    'PriceLocaleModel',
    'PriceModel',
    'SettingsModel',
    'NomenclatureCategoryLocaleModel',
    'NomenclatureCategoryModel',
    'NomenclatureImageModel',
    'NomenclatureLocaleModel',
    'NomenclatureModel',
    'NomenclaturePriceModel',
    'PersonDealAdditionModel',
    'PersonDealAdditionNomenclatureModel',
    'PersonDealModel',
    'PersonImageModel',
    'PersonLocaleModel',
    'PersonModel',
)
