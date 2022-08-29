from decimal import Decimal

from fastapi.applications import FastAPI
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio.scoping import async_scoped_session
from sqlalchemy.sql.schema import MetaData
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from ..models.bonuses.bonus_image_model import BonusImageModel
from ..models.bonuses.bonus_locale_model import BonusLocaleModel
from ..models.bonuses.bonus_model import BonusModel
from ..models.bonuses.categories.bonus_category_model import BonusCategoryModel
from ..models.bonuses.coupons.bonus_coupon_model import BonusCouponModel
from ..models.clients.deals.deal_addition_model import DealAdditionModel
from ..models.clients.deals.deal_addition_nomenclature_model import (
    DealAdditionNomenclatureModel,
)
from ..models.clients.deals.deal_model import DealModel
from ..models.clients.user_model import UserModel
from ..models.containers.container_model import ContainerModel
from ..models.containers.tanks.container_tank_model import ContainerTankModel
from ..models.containers.tanks.container_tank_type_model import (
    ContainerTankTypeModel,
)
from ..models.containers.tanks.operations.container_tank_opening_drop_model import (
    ContainerTankOpeningDropModel,
)
from ..models.containers.tanks.operations.container_tank_opening_model import (
    ContainerTankOpeningModel,
)
from ..models.misc.image_model import ImageModel
from ..models.misc.locales.locale_model import LocaleModel
from ..models.misc.measurements.measurement_model import MeasurementModel
from ..models.misc.prices.price_model import PriceModel
from ..models.misc.settings_model import SettingsModel
from ..models.nomenclatures.categories.nomenclature_category_model import (
    NomenclatureCategoryModel,
)
from ..models.nomenclatures.nomenclature_model import NomenclatureModel
from ..models.nomenclatures.nomenclature_price_model import (
    NomenclaturePriceModel,
)


async def test_database(request: Request, /) -> Response:
    if not isinstance(app := request.get('app'), FastAPI):
        raise HTTPException(
            HTTP_500_INTERNAL_SERVER_ERROR, 'App is not present.'
        )
    if not isinstance(Session := request.get('Session'), async_scoped_session):
        raise HTTPException(
            HTTP_500_INTERNAL_SERVER_ERROR, 'Session is not present.'
        )
    if not isinstance(metadata := request.get('metadata'), MetaData):
        raise HTTPException(
            HTTP_500_INTERNAL_SERVER_ERROR, 'MetaData is not present.'
        )

    locales = [
        LocaleModel(language_code='uk', country_code='UA'),
        LocaleModel(language_code='en', country_code='US'),
    ]
    for locale in locales:
        Session.add(locale)

    settings = SettingsModel(fallback_locale=locales[0])
    Session.add(settings)

    prices = [
        PriceModel(fallback_name='Для фізичних осіб'),
        PriceModel(fallback_name='Для юридичних осіб'),
    ]
    for price in prices:
        Session.add(price)

    measurement = MeasurementModel(fallback_name='послуга')
    nomenclature_category = NomenclatureCategoryModel(
        fallback_name='Поводження з відходами'
    )
    nomenclatures = [
        NomenclatureModel(
            fallback_name='Відкриття бачка з органікою',
            fallback_description='Поводження з органічними відходами',
            category=nomenclature_category,
            measurement=measurement,
            prices=[
                NomenclaturePriceModel(price=prices[0], value=25),
                NomenclaturePriceModel(price=prices[1], value=30),
            ],
        ),
        NomenclatureModel(
            fallback_name='Відкриття бачка з сухими/змішаними',
            fallback_description='Поводження з сухими/змішаними відходами',
            category=nomenclature_category,
            measurement=measurement,
            prices=[
                NomenclaturePriceModel(price=prices[0], value=20),
                NomenclaturePriceModel(price=prices[1], value=25),
            ],
        ),
    ]
    for nomenclature in nomenclatures:
        Session.add(nomenclature)

    user = UserModel(
        fallback_first_name='Тест',
        phone_number=380683980500,
        deals=[
            DealModel(
                fallback_price=prices[0],
                additions=[
                    DealAdditionModel(
                        price=prices[0],
                        nomenclatures=[
                            DealAdditionNomenclatureModel(
                                amount=10,
                                nomenclature=nomenclatures[0],
                            )
                        ],
                    ),
                    DealAdditionModel(
                        price=prices[0],
                        nomenclatures=[
                            DealAdditionNomenclatureModel(
                                amount=2,
                                nomenclature=nomenclatures[1],
                            )
                        ],
                    ),
                ],
            )
        ],
    )
    Session.add(user)

    tank_measurement = MeasurementModel(fallback_name='літр')
    container_tank_types = [
        ContainerTankTypeModel(
            fallback_name='Органічні',
            volume=240,
            measurement=tank_measurement,
        ),
        ContainerTankTypeModel(
            fallback_name='Сухі/Змішані',
            volume=1100,
            measurement=tank_measurement,
        ),
    ]
    for container_tank_type in container_tank_types:
        Session.add(container_tank_type)

    containers = [
        ContainerModel(latitude=50.451024, longtitude=30.519179),
        ContainerModel(latitude=50.444558, longtitude=30.515420),
        ContainerModel(latitude=50.443930, longtitude=30.512522),
        ContainerModel(latitude=50.445505, longtitude=30.516270),
    ]
    for container in reversed(containers):
        container.tanks = [
            ContainerTankModel(type=container_tank_types[0]),
            ContainerTankModel(type=container_tank_types[1]),
        ]
        Session.add(container)

    openings = [
        ContainerTankOpeningModel(
            user=user,
            tank=container.tanks[0],
            nomenclature=user.deals[0].additions[0].nomenclatures[0],
            drops=[
                ContainerTankOpeningDropModel(volume=Decimal(0.05)),
                ContainerTankOpeningDropModel(volume=Decimal(0.055)),
            ],
        ),
        ContainerTankOpeningModel(
            user=user,
            tank=container.tanks[1],
            nomenclature=user.deals[0].additions[1].nomenclatures[0],
            drops=[
                ContainerTankOpeningDropModel(volume=Decimal(0.01)),
                ContainerTankOpeningDropModel(volume=Decimal(0.015)),
            ],
        ),
    ]
    for opening in openings:
        Session.add(opening)

    company = UserModel(
        id=32434111,
        fallback_first_name='Тест',
        phone_number=380683980499,
    )

    bonus_measurement = MeasurementModel(fallback_name='шт')
    bonus_category = BonusCategoryModel(fallback_name='Їжа')
    bonuses = [
        BonusModel(
            fallback_name='Борщ із печі, зі сливовим соусом',
            images=[
                BonusImageModel(
                    image=ImageModel(url='https://imgur.com/gho8MNj.png')
                )
            ],
            locales=[
                BonusLocaleModel(
                    name='Borscht with creamy leckvar',
                    locale=locales[1],
                )
            ],
        ),
        BonusModel(
            fallback_name='Rose Garden',
            images=[
                BonusImageModel(
                    image=ImageModel(url='https://imgur.com/8WWckD0.png')
                )
            ],
        ),
        BonusModel(
            fallback_name='Тарт з полуницею',
            images=[
                BonusImageModel(
                    image=ImageModel(url='https://imgur.com/fRAIrly.png')
                )
            ],
            locales=[
                BonusLocaleModel(
                    name='Tart with strawberry',
                    locale=locales[1],
                )
            ],
        ),
        BonusModel(
            fallback_name='Окрошка на йогурті',
            images=[
                BonusImageModel(
                    image=ImageModel(url='https://imgur.com/SKdHJuu.png')
                )
            ],
            locales=[
                BonusLocaleModel(
                    name='Okroshka made from yoghurt',
                    locale=locales[1],
                )
            ],
        ),
        BonusModel(
            fallback_name='Чебурек з яловичиною',
            images=[
                BonusImageModel(
                    image=ImageModel(url='https://imgur.com/tQbfjKK.png')
                )
            ],
            locales=[
                BonusLocaleModel(
                    name='Cheburek with beef',
                    locale=locales[1],
                )
            ],
        ),
        BonusModel(
            fallback_name='Піца Маргарита',
            images=[
                BonusImageModel(
                    image=ImageModel(url='https://imgur.com/SXHWfQ3.png')
                )
            ],
        ),
        BonusModel(
            fallback_name='Кава Американо',
            images=[
                BonusImageModel(
                    image=ImageModel(url='https://imgur.com/Y82uDQO.png')
                )
            ],
        ),
        BonusModel(
            fallback_name='Cheesecake',
            images=[
                BonusImageModel(
                    image=ImageModel(url='https://imgur.com/AFoVcqE.png')
                )
            ],
        ),
        BonusModel(
            fallback_name='Еклер Малина-каламансі',
            images=[
                BonusImageModel(
                    image=ImageModel(url='https://imgur.com/pA049oW.png')
                )
            ],
        ),
    ]
    for bonus in bonuses:
        bonus.category = bonus_category
        bonus.measurement = bonus_measurement
        bonus.owner = company
        bonus.coupons = [BonusCouponModel() for _ in range(5)]
        Session.add(bonus)

    await Session.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
