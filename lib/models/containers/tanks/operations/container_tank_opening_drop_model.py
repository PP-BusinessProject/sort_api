from decimal import Decimal
from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Numeric

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
        nullable=False,
        key='opening_id',
    )
    id: Final[Column[int]] = Column(
        'Id',
        Integer,
        primary_key=True,
        autoincrement=True,
        key='id',
    )
    volume: Final[Column[Decimal]] = Column(
        'Volume',
        Numeric(6, 6),
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
