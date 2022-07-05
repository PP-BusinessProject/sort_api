from decimal import Decimal
from typing import TYPE_CHECKING, Final

from sqlalchemy import CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Numeric

from .._mixins import Timestamped
from ..base_interface import Base
from .deal_model import DealModel
from .service_model import ServiceModel

if TYPE_CHECKING:
    from ..containers.container_tank_opening_model import (
        ContainerTankOpeningModel,
    )


class DealServiceModel(Timestamped, Base):
    deal_id: Final[Column[int]] = Column(
        'DealId',
        DealModel.id.type,
        ForeignKey(DealModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
        key='deal_id',
    )
    service_id: Final[Column[int]] = Column(
        'ServiceId',
        ServiceModel.id.type,
        ForeignKey(ServiceModel.id, onupdate='CASCADE', ondelete='RESTRICT'),
        primary_key=True,
        key='service_id',
    )
    amount: Final[Column[Decimal]] = Column(
        'Amount',
        Numeric,
        CheckConstraint('"Amount" > 0'),
        nullable=False,
        default=1,
        key='amount',
    )

    deal: Final['RelationshipProperty[DealModel]'] = relationship(
        'DealModel',
        back_populates='services',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    service: Final['RelationshipProperty[ServiceModel]'] = relationship(
        'ServiceModel',
        back_populates='deals',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    openings: Final[
        'RelationshipProperty[list[ContainerTankOpeningModel]]'
    ] = relationship(
        'ContainerTankOpeningModel',
        back_populates='deal_service',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
