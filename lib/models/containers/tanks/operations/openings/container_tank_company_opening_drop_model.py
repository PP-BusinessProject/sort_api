from decimal import Decimal
from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Numeric

from ....._mixins import Timestamped
from .....base_interface import Base
from .container_tank_company_opening_model import (
    ContainerTankCompanyOpeningModel,
)


class ContainerTankCompanyOpeningDropModel(Timestamped, Base):
    opening_id: Final[Column[int]] = Column(
        ContainerTankCompanyOpeningModel.id.type,
        ForeignKey(
            ContainerTankCompanyOpeningModel.id,
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
        'RelationshipProperty[ContainerTankCompanyOpeningModel]'
    ] = relationship(
        'ContainerTankCompanyOpeningModel',
        back_populates='drops',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
