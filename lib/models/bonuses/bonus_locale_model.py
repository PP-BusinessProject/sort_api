from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import String

from .._mixins import Timestamped
from ..base_interface import Base
from ..misc.locales.locale_model import LocaleModel
from .bonus_model import BonusModel


class BonusLocaleModel(Timestamped, Base):
    bonus_id: Final[Column[str]] = Column(
        'BonusId',
        BonusModel.id.type,
        ForeignKey(BonusModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
        key='bonus_id',
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
    description: Final[Column[str]] = Column(
        'Description',
        String(1023),
        nullable=False,
        default='',
        key='description',
    )

    locale: Final['RelationshipProperty[LocaleModel]'] = relationship(
        'LocaleModel',
        back_populates='bonus_locales',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    bonus: Final['RelationshipProperty[BonusModel]'] = relationship(
        'BonusModel',
        back_populates='locales',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
