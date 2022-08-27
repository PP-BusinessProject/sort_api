from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import String

from ..._mixins import Timestamped
from ...base_interface import Base
from ..locales.locale_model import LocaleModel
from .price_model import PriceModel


class PriceLocaleModel(Timestamped, Base):
    price_id: Final[Column[str]] = Column(
        'PriceId',
        PriceModel.id.type,
        ForeignKey(PriceModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
        key='price_id',
    )
    locale_alpha_2: Final[Column[str]] = Column(
        'LocaleAlpha2',
        LocaleModel.alpha_2.type,
        ForeignKey(
            LocaleModel.alpha_2,
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
        primary_key=True,
        key='locale_alpha_2',
    )

    name: Final[Column[str]] = Column(
        'Name',
        String(255),
        CheckConstraint('"Name" <> \'\''),
        nullable=False,
        key='name',
    )

    locale: Final['RelationshipProperty[LocaleModel]'] = relationship(
        'LocaleModel',
        back_populates='price_locales',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    price: Final['RelationshipProperty[PriceModel]'] = relationship(
        'PriceModel',
        back_populates='locales',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
