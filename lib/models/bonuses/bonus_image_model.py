from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey

from .._mixins import Timestamped
from ..base_interface import Base
from ..misc.image_model import ImageModel
from .bonus_model import BonusModel


class BonusImageModel(Timestamped, Base):
    bonus_id: Final[Column[int]] = Column(
        BonusModel.id.type,
        ForeignKey(BonusModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
    )
    image_id: Final[Column[int]] = Column(
        ImageModel.id.type,
        ForeignKey(ImageModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
    )

    bonus: Final['RelationshipProperty[BonusModel]'] = relationship(
        'BonusModel',
        back_populates='images',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    image: Final['RelationshipProperty[ImageModel]'] = relationship(
        'ImageModel',
        back_populates='bonuses',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
