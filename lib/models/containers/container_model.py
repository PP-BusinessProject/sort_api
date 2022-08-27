from decimal import Decimal
from typing import TYPE_CHECKING, Final, Optional

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Numeric, SmallInteger

from .._mixins import Timestamped
from ..base_interface import Base
from ..clients.user_model import UserModel
from ..misc.addresses.address_model import AddressModel

if TYPE_CHECKING:
    from .container_image_model import ContainerImageModel
    from .reports.container_report_model import ContainerReportModel
    from .tanks.container_tank_model import ContainerTankModel


class ContainerModel(Timestamped, Base):
    owner_id: Final[Column[Optional[int]]] = Column(
        'OwnerId',
        UserModel.id.type,
        ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='SET NULL'),
        key='owner_id',
    )
    id: Final[Column[int]] = Column(
        'Id',
        SmallInteger,
        primary_key=True,
        autoincrement=True,
        key='id',
    )
    latitude: Final[Column[Decimal]] = Column(
        'Latitude',
        Numeric(8, 6),
        nullable=False,
        key='latitude',
    )
    longtitude: Final[Column[Decimal]] = Column(
        'Longtitude',
        Numeric(9, 6),
        nullable=False,
        key='longtitude',
    )
    address_id: Final[Column[Optional[int]]] = Column(
        'AddressId',
        AddressModel.id.type,
        ForeignKey(AddressModel.id, onupdate='CASCADE', ondelete='RESTRICT'),
        key='address_id',
    )

    owner: Final['RelationshipProperty[UserModel]'] = relationship(
        'UserModel',
        back_populates='containers',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    address: Final['RelationshipProperty[AddressModel]'] = relationship(
        'AddressModel',
        back_populates='containers',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    images: Final[
        'RelationshipProperty[list[ContainerImageModel]]'
    ] = relationship(
        'ContainerImageModel',
        back_populates='container',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    tanks: Final[
        'RelationshipProperty[list[ContainerTankModel]]'
    ] = relationship(
        'ContainerTankModel',
        back_populates='container',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    reports: Final[
        'RelationshipProperty[list[ContainerReportModel]]'
    ] = relationship(
        'ContainerReportModel',
        back_populates='container',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
