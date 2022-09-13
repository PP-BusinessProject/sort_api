from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column
from sqlalchemy.sql.sqltypes import Integer, String

from .._mixins import Timestamped
from ..base_interface import Base

if TYPE_CHECKING:
    from ..bonuses.bonus_image_model import BonusImageModel

    from ..containers.container_image_model import ContainerImageModel
    from ..nomenclatures.nomenclature_image_model import NomenclatureImageModel


class ImageModel(Timestamped, Base):
    id: Final[Column[int]] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    url: Final[Column[str]] = Column(
        String(2048),
        CheckConstraint("url <> ''"),
        nullable=False,
    )

    bonuses: Final[
        'RelationshipProperty[list[BonusImageModel]]'
    ] = relationship(
        'BonusImageModel',
        back_populates='image',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    containers: Final[
        'RelationshipProperty[list[ContainerImageModel]]'
    ] = relationship(
        'ContainerImageModel',
        back_populates='image',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    nomenclatures: Final[
        'RelationshipProperty[list[NomenclatureImageModel]]'
    ] = relationship(
        'NomenclatureImageModel',
        back_populates='image',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
