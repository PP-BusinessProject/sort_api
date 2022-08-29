from decimal import Decimal
from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Numeric

from .._mixins import Timestamped
from ..base_interface import Base
from ..misc.prices.price_model import PriceModel
from .nomenclature_model import NomenclatureModel


class NomenclaturePriceModel(Timestamped, Base):
    nomenclature_id: Final[Column[int]] = Column(
        'NomenclatureId',
        NomenclatureModel.id.type,
        ForeignKey(
            NomenclatureModel.id,
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        primary_key=True,
        key='nomenclature_id',
    )
    price_id: Final[Column[int]] = Column(
        'PriceId',
        PriceModel.id.type,
        ForeignKey(PriceModel.id, onupdate='CASCADE', ondelete='RESTRICT'),
        primary_key=True,
        key='price_id',
    )
    value: Final[Column[Decimal]] = Column(
        'Value',
        Numeric(8, 2),
        CheckConstraint('"Value" >= 0'),
        nullable=False,
        key='value',
    )

    nomenclature: Final[
        'RelationshipProperty[NomenclatureModel]'
    ] = relationship(
        'NomenclatureModel',
        back_populates='prices',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    price: Final['RelationshipProperty[PriceModel]'] = relationship(
        'PriceModel',
        back_populates='nomenclatures',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
