from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import String

from ...base_interface import Base
from .address_model import AddressModel
from ..locales.locale_model import LocaleModel


class AddressLocaleModel(Base):
    address_id: Final[Column[int]] = Column(
        'AddressId',
        ForeignKey(
            AddressModel.id,
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        primary_key=True,
        autoincrement=True,
        key='address_id',
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

    country: Final[Column[str]] = Column(
        'Сountry',
        String(255),
        CheckConstraint('"Сountry" <> \'\''),
        nullable=False,
        default='Ukraine',
        key='country',
    )
    state: Final[Column[str]] = Column(
        'State',
        String(255),
        CheckConstraint('"State" <> \'\''),
        nullable=False,
        key='state',
    )
    city: Final[Column[str]] = Column(
        'City',
        String(255),
        CheckConstraint('"City" <> \'\''),
        nullable=False,
        key='city',
    )
    street: Final[Column[str]] = Column(
        'Street',
        String(255),
        CheckConstraint('"Street" <> \'\''),
        nullable=False,
        key='street',
    )

    locale: Final['RelationshipProperty[LocaleModel]'] = relationship(
        'LocaleModel',
        back_populates='address_locales',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    address: Final['RelationshipProperty[AddressModel]'] = relationship(
        'AddressModel',
        back_populates='locales',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
