from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column
from sqlalchemy.sql.sqltypes import Integer, String

from .._mixins import Timestamped
from ..base_interface import Base

if TYPE_CHECKING:
    from ..bonuses.bonus_image_model import BonusImageModel


class ImageModel(Timestamped, Base):
    id: Final[Column[int]] = Column(
        'Id',
        Integer,
        primary_key=True,
        autoincrement=True,
        key='id',
    )
    url: Final[Column[str]] = Column(
        'Url',
        String(2048),
        CheckConstraint('"Url" <> \'\''),
        nullable=False,
        key='url',
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
