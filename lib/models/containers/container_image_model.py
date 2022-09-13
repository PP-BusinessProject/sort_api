from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey

from .._mixins import Timestamped
from ..base_interface import Base
from ..misc.image_model import ImageModel
from .container_model import ContainerModel


class ContainerImageModel(Timestamped, Base):
    container_id: Final[Column[int]] = Column(
        ContainerModel.id.type,
        ForeignKey(ContainerModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
    )
    image_id: Final[Column[int]] = Column(
        ImageModel.id.type,
        ForeignKey(ImageModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
    )

    container: Final['RelationshipProperty[ContainerModel]'] = relationship(
        'ContainerModel',
        back_populates='images',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    image: Final['RelationshipProperty[ImageModel]'] = relationship(
        'ImageModel',
        back_populates='containers',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
