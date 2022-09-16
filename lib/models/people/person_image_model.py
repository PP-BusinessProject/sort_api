from typing import Final
from uuid import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey

from .._mixins import Timestamped
from ..base_interface import Base
from ..misc.image_model import ImageModel
from .person_model import PersonModel


class PersonImageModel(Timestamped, Base):
    company_id: Final[Column[UUID]] = Column(
        PersonModel.user_id.type,
        ForeignKey(
            PersonModel.user_id, onupdate='CASCADE', ondelete='CASCADE'
        ),
        primary_key=True,
    )
    image_id: Final[Column[int]] = Column(
        ImageModel.id.type,
        ForeignKey(ImageModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
    )

    person: Final['RelationshipProperty[PersonModel]'] = relationship(
        'PersonModel',
        back_populates='images',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    image: Final['RelationshipProperty[ImageModel]'] = relationship(
        'ImageModel',
        back_populates='people',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
