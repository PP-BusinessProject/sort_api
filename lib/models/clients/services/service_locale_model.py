from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import String

from ...base_interface import Base
from ...misc.locales.locale_model import LocaleModel
from .service_model import ServiceModel


class ServiceLocaleModel(Base):
    service_id: Final[Column[int]] = Column(
        'ServiceId',
        ServiceModel.id.type,
        ForeignKey(ServiceModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
        key='service_id',
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
        key='description',
    )

    locale: Final['RelationshipProperty[LocaleModel]'] = relationship(
        'LocaleModel',
        back_populates='service_locales',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    service: Final['RelationshipProperty[ServiceModel]'] = relationship(
        'ServiceModel',
        back_populates='locales',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
