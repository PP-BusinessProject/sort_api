from decimal import Decimal
from uuid import UUID

from fastapi.applications import FastAPI
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio.scoping import async_scoped_session
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.schema import MetaData
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import (
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from ..models.auth.user_model import UserModel
from ..models.companies.bonuses.categories.company_bonus_category_model import (
    CompanyBonusCategoryModel,
)
from ..models.companies.bonuses.company_bonus_image_model import (
    CompanyBonusImageModel,
)
from ..models.companies.bonuses.company_bonus_locale_model import (
    CompanyBonusLocaleModel,
)
from ..models.companies.bonuses.company_bonus_model import CompanyBonusModel
from ..models.companies.bonuses.coupons.company_bonus_coupon_model import (
    CompanyBonusCouponModel,
)
from ..models.companies.company_model import CompanyModel
from ..models.containers.container_model import ContainerModel
from ..models.containers.tanks.container_tank_model import ContainerTankModel
from ..models.containers.tanks.container_tank_type_model import (
    ContainerTankTypeModel,
)
from ..models.containers.tanks.operations.openings.container_tank_person_opening_drop_model import (
    ContainerTankPersonOpeningDropModel,
)
from ..models.containers.tanks.operations.openings.container_tank_person_opening_model import (
    ContainerTankPersonOpeningModel,
)
from ..models.misc.addresses.address_model import AddressModel
from ..models.misc.banks.bank_model import BankModel
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
from ..models.people.deals.additions.person_deal_addition_model import (
    PersonDealAdditionModel,
)
from ..models.people.deals.additions.person_deal_addition_nomenclature_model import (
    PersonDealAdditionNomenclatureModel,
)
from ..models.people.deals.person_deal_model import PersonDealModel
from ..models.people.person_model import PersonModel


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

    if (user := await Session.scalar(select(UserModel))) is None:
        raise HTTPException(HTTP_404_NOT_FOUND, 'User is not found.')
    person = PersonModel(
        user=user,
        fallback_first_name='Тест',
        deals=[
            PersonDealModel(
                fallback_price=prices[0],
                additions=[
                    PersonDealAdditionModel(
                        price=prices[0],
                        nomenclatures=[
                            PersonDealAdditionNomenclatureModel(
                                amount=10,
                                nomenclature=nomenclatures[0],
                            )
                        ],
                    ),
                    PersonDealAdditionModel(
                        price=prices[0],
                        nomenclatures=[
                            PersonDealAdditionNomenclatureModel(
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
        ContainerTankPersonOpeningModel(
            person=person,
            tank=container.tanks[0],
            nomenclature=person.deals[0].additions[0].nomenclatures[0],
            drops=[
                ContainerTankPersonOpeningDropModel(volume=Decimal(0.05)),
                ContainerTankPersonOpeningDropModel(volume=Decimal(0.055)),
            ],
        ),
        ContainerTankPersonOpeningModel(
            person=person,
            tank=container.tanks[1],
            nomenclature=person.deals[0].additions[1].nomenclatures[0],
            drops=[
                ContainerTankPersonOpeningDropModel(volume=Decimal(0.01)),
                ContainerTankPersonOpeningDropModel(volume=Decimal(0.015)),
            ],
        ),
    ]
    for opening in openings:
        Session.add(opening)

    company = CompanyModel(
        user=user,
        registry_number=32434111,
        fallback_name='Тест',
        bank_account_number='UA734578698374659436987543229',
        address=AddressModel(
            fallback_state='Дніпропетровська область',
            fallback_city='Дніпро',
            fallback_street='вул. Центральна',
            building=10,
            postal_code=49000,
        ),
        bank=BankModel(
            code='12345678',
            fallback_name='НБУ',
            address=AddressModel(
                fallback_state='Дніпропетровська область',
                fallback_city='Дніпро',
                fallback_street='вул. Центральна',
                building=20,
                postal_code=49000,
            ),
        ),
    )

    bonus_measurement = MeasurementModel(fallback_name='шт')
    bonus_category = CompanyBonusCategoryModel(fallback_name='Їжа')
    bonuses = [
        CompanyBonusModel(
            fallback_name='Борщ із печі, зі сливовим соусом',
            images=[
                CompanyBonusImageModel(
                    image=ImageModel(url='https://imgur.com/gho8MNj.png')
                )
            ],
            locales=[
                CompanyBonusLocaleModel(
                    name='Borscht with creamy leckvar',
                    locale=locales[1],
                )
            ],
        ),
        CompanyBonusModel(
            fallback_name='Rose Garden',
            images=[
                CompanyBonusImageModel(
                    image=ImageModel(url='https://imgur.com/8WWckD0.png')
                )
            ],
        ),
        CompanyBonusModel(
            fallback_name='Тарт з полуницею',
            images=[
                CompanyBonusImageModel(
                    image=ImageModel(url='https://imgur.com/fRAIrly.png')
                )
            ],
            locales=[
                CompanyBonusLocaleModel(
                    name='Tart with strawberry',
                    locale=locales[1],
                )
            ],
        ),
        CompanyBonusModel(
            fallback_name='Окрошка на йогурті',
            images=[
                CompanyBonusImageModel(
                    image=ImageModel(url='https://imgur.com/SKdHJuu.png')
                )
            ],
            locales=[
                CompanyBonusLocaleModel(
                    name='Okroshka made from yoghurt',
                    locale=locales[1],
                )
            ],
        ),
        CompanyBonusModel(
            fallback_name='Чебурек з яловичиною',
            images=[
                CompanyBonusImageModel(
                    image=ImageModel(url='https://imgur.com/tQbfjKK.png')
                )
            ],
            locales=[
                CompanyBonusLocaleModel(
                    name='Cheburek with beef',
                    locale=locales[1],
                )
            ],
        ),
        CompanyBonusModel(
            fallback_name='Піца Маргарита',
            images=[
                CompanyBonusImageModel(
                    image=ImageModel(url='https://imgur.com/SXHWfQ3.png')
                )
            ],
        ),
        CompanyBonusModel(
            fallback_name='Кава Американо',
            images=[
                CompanyBonusImageModel(
                    image=ImageModel(url='https://imgur.com/Y82uDQO.png')
                )
            ],
        ),
        CompanyBonusModel(
            fallback_name='Cheesecake',
            images=[
                CompanyBonusImageModel(
                    image=ImageModel(url='https://imgur.com/AFoVcqE.png')
                )
            ],
        ),
        CompanyBonusModel(
            fallback_name='Еклер Малина-каламансі',
            images=[
                CompanyBonusImageModel(
                    image=ImageModel(url='https://imgur.com/pA049oW.png')
                )
            ],
        ),
    ]
    for bonus in bonuses:
        bonus.category = bonus_category
        bonus.measurement = bonus_measurement
        bonus.company = company
        bonus.coupons = [CompanyBonusCouponModel() for _ in range(5)]
        Session.add(bonus)

    await Session.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
