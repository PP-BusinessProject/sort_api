from decimal import Decimal
from typing import TYPE_CHECKING, Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Numeric

from ..._mixins import Timestamped
from ...base_interface import Base
from ..container_model import ContainerModel
from .container_tank_type_model import ContainerTankTypeModel

if TYPE_CHECKING:
    # from .operations.container_tank_clearing_model import (
    #     ContainerTankClearingModel,
    # )
    from .operations.openings.container_tank_company_opening_model import (
        ContainerTankCompanyOpeningModel,
    )
    from .operations.openings.container_tank_person_opening_model import (
        ContainerTankPersonOpeningModel,
    )


class ContainerTankModel(Timestamped, Base):
    container_id: Final[Column[int]] = Column(
        ContainerModel.id.type,
        ForeignKey(ContainerModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
    )
    type_id: Final[Column[int]] = Column(
        ContainerTankTypeModel.id.type,
        ForeignKey(
            ContainerTankTypeModel.id,
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        primary_key=True,
    )
    current_volume: Final[Column[Decimal]] = Column(
        Numeric(8, 8),
        nullable=False,
        default=Decimal(),
    )

    container: Final['RelationshipProperty[ContainerModel]'] = relationship(
        'ContainerModel',
        back_populates='tanks',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    type: Final['RelationshipProperty[ContainerTankTypeModel]'] = relationship(
        'ContainerTankTypeModel',
        back_populates='tanks',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    company_openings: Final[
        'RelationshipProperty[list[ContainerTankCompanyOpeningModel]]'
    ] = relationship(
        'ContainerTankCompanyOpeningModel',
        back_populates='tank',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    person_openings: Final[
        'RelationshipProperty[list[ContainerTankPersonOpeningModel]]'
    ] = relationship(
        'ContainerTankPersonOpeningModel',
        back_populates='tank',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    # clearings: Final[
    #     'RelationshipProperty[list[ContainerTankClearingModel]]'
    # ] = relationship(
    #     'ContainerTankClearingModel',
    #     back_populates='tank',
    #     lazy='noload',
    #     cascade='save-update, merge, expunge, delete, delete-orphan',
    #     uselist=True,
    # )
