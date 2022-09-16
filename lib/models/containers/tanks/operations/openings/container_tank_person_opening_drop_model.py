from decimal import Decimal
from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Numeric

from ....._mixins import Timestamped
from .....base_interface import Base
from .container_tank_person_opening_model import (
    ContainerTankPersonOpeningModel,
)


class ContainerTankPersonOpeningDropModel(Timestamped, Base):
    opening_id: Final[Column[int]] = Column(
        ContainerTankPersonOpeningModel.id.type,
        ForeignKey(
            ContainerTankPersonOpeningModel.id,
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        nullable=False,
    )
    id: Final[Column[int]] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    volume: Final[Column[Decimal]] = Column(
        Numeric(6, 6),
        nullable=False,
    )

    opening: Final[
        'RelationshipProperty[ContainerTankPersonOpeningModel]'
    ] = relationship(
        'ContainerTankPersonOpeningModel',
        back_populates='drops',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
