from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column
from sqlalchemy.sql.sqltypes import Integer, String

from .._mixins import Timestamped
from ..base_interface import Base

if TYPE_CHECKING:
    from ..companies.bonuses.company_bonus_image_model import (
        CompanyBonusImageModel,
    )
    from ..companies.company_image_model import CompanyImageModel
    from ..containers.container_image_model import ContainerImageModel
    from ..nomenclatures.nomenclature_image_model import NomenclatureImageModel
    from ..people.person_image_model import PersonImageModel


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

    companies: Final[
        'RelationshipProperty[list[CompanyImageModel]]'
    ] = relationship(
        'CompanyImageModel',
        back_populates='image',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    company_bonuses: Final[
        'RelationshipProperty[list[CompanyBonusImageModel]]'
    ] = relationship(
        'CompanyBonusImageModel',
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
    people: Final[
        'RelationshipProperty[list[PersonImageModel]]'
    ] = relationship(
        'PersonImageModel',
        back_populates='image',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
