from typing import Final, Tuple

from ._mixins import Timestamped
from .base_interface import BaseInterface
from .bonuses import (
    BonusCouponModel,
    BonusImageModel,
    BonusModel,
    BonusPriceModel,
)
from .clients import (
    CompanyModel,
    DealModel,
    DealServiceModel,
    GroupMemberModel,
    GroupModel,
    GroupRights,
    PersonModel,
    ServiceModel,
    ServicePriceModel,
    UserModel,
)
from .containers import (
    ContainerModel,
    ContainerReportModel,
    ContainerReportTypeModel,
    ContainerTankClearingModel,
    ContainerTankModel,
    ContainerTankOpeningDropModel,
    ContainerTankOpeningModel,
    ContainerTankTypeModel,
)
from .deliveries import DeliveryModel, DeliveryServiceModel
from .locales import LocaleModel, LocaleTextModel, TextModel
from .misc import (
    AddressModel,
    BankModel,
    ImageModel,
    MeasurementModel,
    PriceModel,
    SettingsModel,
)
from .user_interface import UserInterface

__all__: Final[Tuple[str, ...]] = (
    'Timestamped',
    'BaseInterface',
    'BonusCouponModel',
    'BonusImageModel',
    'BonusModel',
    'BonusPriceModel',
    'CompanyModel',
    'DealModel',
    'DealServiceModel',
    'GroupMemberModel',
    'GroupModel',
    'GroupRights',
    'PersonModel',
    'ServiceModel',
    'ServicePriceModel',
    'UserModel',
    'ContainerModel',
    'ContainerReportModel',
    'ContainerReportTypeModel',
    'ContainerTankClearingModel',
    'ContainerTankModel',
    'ContainerTankOpeningDropModel',
    'ContainerTankOpeningModel',
    'ContainerTankTypeModel',
    'DeliveryModel',
    'DeliveryServiceModel',
    'LocaleModel',
    'LocaleTextModel',
    'TextModel',
    'AddressModel',
    'BankModel',
    'ImageModel',
    'MeasurementModel',
    'PriceModel',
    'SettingsModel',
    'UserInterface',
)
