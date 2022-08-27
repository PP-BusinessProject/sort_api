from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from ...._mixins import Timestamped
from ....base_interface import Base
from .container_tank_opening_model import ContainerTankOpeningModel


class ContainerTankOpeningDropModel(Timestamped, Base):
    opening_id: Final[Column[int]] = Column(
        'OpeningId',
        ContainerTankOpeningModel.id.type,
        ForeignKey(
            ContainerTankOpeningModel.id,
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        primary_key=True,
        key='opening_id',
    )
    volume: Final[Column[int]] = Column(
        'Volume',
        Integer,
        nullable=False,
        key='volume',
    )

    opening: Final[
        'RelationshipProperty[ContainerTankOpeningModel]'
    ] = relationship(
        'ContainerTankOpeningModel',
        back_populates='drops',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
