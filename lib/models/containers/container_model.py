from decimal import Decimal
from typing import TYPE_CHECKING, Final, Optional

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Numeric, SmallInteger

from .._mixins import Timestamped
from ..base_interface import Base
from ..companies.company_model import CompanyModel
from ..misc.addresses.address_model import AddressModel

if TYPE_CHECKING:
    from .container_image_model import ContainerImageModel
    from .reports.container_report_model import ContainerReportModel
    from .tanks.container_tank_model import ContainerTankModel


class ContainerModel(Timestamped, Base):
    owner_id: Final[Column[Optional[int]]] = Column(
        CompanyModel.user_id.type,
        ForeignKey(
            CompanyModel.user_id, onupdate='CASCADE', ondelete='SET NULL'
        ),
    )
    id: Final[Column[int]] = Column(
        SmallInteger,
        primary_key=True,
        autoincrement=True,
    )
    latitude: Final[Column[Decimal]] = Column(
        Numeric(8, 6),
        nullable=False,
    )
    longtitude: Final[Column[Decimal]] = Column(
        Numeric(9, 6),
        nullable=False,
    )
    address_id: Final[Column[Optional[int]]] = Column(
        AddressModel.id.type,
        ForeignKey(AddressModel.id, onupdate='CASCADE', ondelete='RESTRICT'),
    )

    owner: Final[
        'RelationshipProperty[Optional[CompanyModel]]'
    ] = relationship(
        'CompanyModel',
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
