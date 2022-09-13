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
        NomenclatureModel.id.type,
        ForeignKey(
            NomenclatureModel.id,
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        primary_key=True,
    )
    price_id: Final[Column[int]] = Column(
        PriceModel.id.type,
        ForeignKey(PriceModel.id, onupdate='CASCADE', ondelete='RESTRICT'),
        primary_key=True,
    )
    value: Final[Column[Decimal]] = Column(
        Numeric(8, 2),
        CheckConstraint('value >= 0'),
        nullable=False,
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
