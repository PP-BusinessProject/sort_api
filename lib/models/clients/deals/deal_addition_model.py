"""The module that provides a `DealModel`."""


from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, Integer

from ..._mixins import Timestamped
from ...base_interface import Base
from ...misc.prices.price_model import PriceModel
from .deal_model import DealModel

if TYPE_CHECKING:
    from .deal_addition_nomenclature_model import DealAdditionNomenclatureModel


class DealAdditionModel(Timestamped, Base):

    deal_id: Final[Column[int]] = Column(
        DealModel.id.type,
        ForeignKey(DealModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
    )
    id: Final[Column[int]] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    price_id: Final[Column[int]] = Column(
        PriceModel.id.type,
        ForeignKey(PriceModel.id, onupdate='CASCADE', ondelete='RESTRICT'),
        nullable=False,
    )
    payment_type: Final[Column[bool]] = Column(
        Boolean(create_constraint=True),
        nullable=False,
        default=False,
        doc='Prepayment (False) or Payment (True).',
    )

    deal: Final['RelationshipProperty[DealModel]'] = relationship(
        'DealModel',
        back_populates='additions',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    price: Final['RelationshipProperty[PriceModel]'] = relationship(
        'PriceModel',
        back_populates='deal_additions',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    nomenclatures: Final[
        'RelationshipProperty[list[DealAdditionNomenclatureModel]]'
    ] = relationship(
        'DealAdditionNomenclatureModel',
        back_populates='addition',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
