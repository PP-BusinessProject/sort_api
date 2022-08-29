from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey

from .._mixins import Timestamped
from ..base_interface import Base
from ..misc.image_model import ImageModel
from .nomenclature_model import NomenclatureModel


class NomenclatureImageModel(Timestamped, Base):
    nomenclature_id: Final[Column[int]] = Column(
        'NomenclatureId',
        NomenclatureModel.id.type,
        ForeignKey(
            NomenclatureModel.id,
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        primary_key=True,
        key='nomenclature_id',
    )
    image_id: Final[Column[int]] = Column(
        'ImageId',
        ImageModel.id.type,
        ForeignKey(ImageModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
        key='image_id',
    )

    nomenclature: Final[
        'RelationshipProperty[NomenclatureModel]'
    ] = relationship(
        'NomenclatureModel',
        back_populates='images',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    image: Final['RelationshipProperty[ImageModel]'] = relationship(
        'ImageModel',
        back_populates='nomenclatures',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
