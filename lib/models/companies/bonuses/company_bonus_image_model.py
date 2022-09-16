from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey

from ..._mixins import Timestamped
from ...base_interface import Base
from ...misc.image_model import ImageModel
from .company_bonus_model import CompanyBonusModel


class CompanyBonusImageModel(Timestamped, Base):
    bonus_id: Final[Column[int]] = Column(
        CompanyBonusModel.id.type,
        ForeignKey(
            CompanyBonusModel.id, onupdate='CASCADE', ondelete='CASCADE'
        ),
        primary_key=True,
    )
    image_id: Final[Column[int]] = Column(
        ImageModel.id.type,
        ForeignKey(ImageModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
    )

    bonus: Final['RelationshipProperty[CompanyBonusModel]'] = relationship(
        'CompanyBonusModel',
        back_populates='images',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    image: Final['RelationshipProperty[ImageModel]'] = relationship(
        'ImageModel',
        back_populates='company_bonuses',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
