from typing import Final
from uuid import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey

from .._mixins import Timestamped
from ..base_interface import Base
from ..misc.image_model import ImageModel
from .company_model import CompanyModel


class CompanyImageModel(Timestamped, Base):
    company_id: Final[Column[UUID]] = Column(
        CompanyModel.user_id.type,
        ForeignKey(
            CompanyModel.user_id, onupdate='CASCADE', ondelete='CASCADE'
        ),
        primary_key=True,
    )
    image_id: Final[Column[int]] = Column(
        ImageModel.id.type,
        ForeignKey(ImageModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
    )

    company: Final['RelationshipProperty[CompanyModel]'] = relationship(
        'CompanyModel',
        back_populates='images',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    image: Final['RelationshipProperty[ImageModel]'] = relationship(
        'ImageModel',
        back_populates='companies',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
