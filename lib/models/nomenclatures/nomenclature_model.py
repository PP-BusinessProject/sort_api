from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from ..base_interface import Base
from ..misc.measurements.measurement_model import MeasurementModel
from .categories.nomenclature_category_model import NomenclatureCategoryModel

if TYPE_CHECKING:
    from ..companies.deals.additions.company_deal_addition_nomenclature_model import (
        CompanyDealAdditionNomenclatureModel,
    )
    from ..people.deals.additions.person_deal_addition_nomenclature_model import (
        PersonDealAdditionNomenclatureModel,
    )

    # from ..deliveries.delivery_nomenclature_model import (
    #     DeliveryNomenclatureModel,
    # )
    from .nomenclature_image_model import NomenclatureImageModel
    from .nomenclature_locale_model import NomenclatureLocaleModel
    from .nomenclature_price_model import NomenclaturePriceModel


class NomenclatureModel(Base):
    id: Final[Column[int]] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    fallback_name: Final[Column[str]] = Column(
        String(255),
        CheckConstraint("fallback_name <> ''"),
        nullable=False,
    )
    fallback_description: Final[Column[str]] = Column(
        String(1023),
        nullable=False,
        default='',
    )
    category_id: Final[Column[int]] = Column(
        NomenclatureCategoryModel.id.type,
        ForeignKey(
            NomenclatureCategoryModel.id,
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
        nullable=False,
    )
    measurement_id: Final[Column[int]] = Column(
        MeasurementModel.id.type,
        ForeignKey(
            MeasurementModel.id,
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
        nullable=False,
    )

    locales: Final[
        'RelationshipProperty[list[NomenclatureLocaleModel]]'
    ] = relationship(
        'NomenclatureLocaleModel',
        back_populates='nomenclature',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    images: Final[
        'RelationshipProperty[list[NomenclatureImageModel]]'
    ] = relationship(
        'NomenclatureImageModel',
        back_populates='nomenclature',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    category: Final[
        'RelationshipProperty[NomenclatureCategoryModel]'
    ] = relationship(
        'NomenclatureCategoryModel',
        back_populates='nomenclatures',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    measurement: Final[
        'RelationshipProperty[MeasurementModel]'
    ] = relationship(
        'MeasurementModel',
        back_populates='nomenclatures',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    prices: Final[
        'RelationshipProperty[list[NomenclaturePriceModel]]'
    ] = relationship(
        'NomenclaturePriceModel',
        back_populates='nomenclature',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )

    company_deal_additions: Final[
        'RelationshipProperty[list[CompanyDealAdditionNomenclatureModel]]'
    ] = relationship(
        'CompanyDealAdditionNomenclatureModel',
        back_populates='nomenclature',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    person_deal_additions: Final[
        'RelationshipProperty[list[PersonDealAdditionNomenclatureModel]]'
    ] = relationship(
        'PersonDealAdditionNomenclatureModel',
        back_populates='nomenclature',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    # deliveries: Final[
    #     'RelationshipProperty[list[DeliveryNomenclatureModel]]'
    # ] = relationship(
    #     'DeliveryNomenclatureModel',
    #     back_populates='nomenclature',
    #     lazy='noload',
    #     cascade='save-update, merge, expunge, delete, delete-orphan',
    #     uselist=True,
    # )
