from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from ..base_interface import Base
from ..misc.measurements.measurement_model import MeasurementModel
from .categories.nomenclature_category_model import NomenclatureCategoryModel

if TYPE_CHECKING:
    from ..clients.deals.deal_addition_nomenclature_model import (
        DealAdditionNomenclatureModel,
    )
    from ..deliveries.delivery_nomenclature_model import (
        DeliveryNomenclatureModel,
    )
    from .nomenclature_image_model import NomenclatureImageModel
    from .nomenclature_locale_model import NomenclatureLocaleModel
    from .nomenclature_price_model import NomenclaturePriceModel


class NomenclatureModel(Base):
    id: Final[Column[int]] = Column(
        'Id',
        Integer,
        primary_key=True,
        autoincrement=True,
        key='id',
    )
    fallback_name: Final[Column[str]] = Column(
        'FallbackName',
        String(255),
        CheckConstraint('"FallbackName" <> \'\''),
        nullable=False,
        key='fallback_name',
    )
    fallback_description: Final[Column[str]] = Column(
        'FallbackDescription',
        String(1023),
        nullable=False,
        default='',
        key='fallback_description',
    )
    category_id: Final[Column[int]] = Column(
        'CategoryId',
        NomenclatureCategoryModel.id.type,
        ForeignKey(
            NomenclatureCategoryModel.id,
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
        nullable=False,
        key='category_id',
    )
    measurement_id: Final[Column[int]] = Column(
        'MeasurementId',
        MeasurementModel.id.type,
        ForeignKey(
            MeasurementModel.id,
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
        nullable=False,
        key='measurement_id',
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
    deal_additions: Final[
        'RelationshipProperty[list[DealAdditionNomenclatureModel]]'
    ] = relationship(
        'DealAdditionNomenclatureModel',
        back_populates='nomenclature',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    deliveries: Final[
        'RelationshipProperty[list[DeliveryNomenclatureModel]]'
    ] = relationship(
        'DeliveryNomenclatureModel',
        back_populates='nomenclature',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
