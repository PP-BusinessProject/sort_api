from typing import TYPE_CHECKING, Final, Type

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.expression import ClauseElement, and_, literal_column
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer
from typing_extensions import Self

from .._mixins import Timestamped
from ..base_interface import Base
from ..user_interface import UserInterface

if TYPE_CHECKING:
    from ..bonuses.bonus_model import BonusModel
    from ..containers.container_model import ContainerModel
    from ..containers.tanks.operations.container_tank_clearing_model import (
        ContainerTankClearingModel,
    )
    from ..containers.tanks.operations.container_tank_opening_model import (
        ContainerTankOpeningModel,
    )
    from .companies.company_model import CompanyModel
    from .deals.deal_model import DealModel
    from .groups.group_model import GroupModel
    from .person_model import PersonModel
    from .user_locale_model import UserLocaleModel


class UserModel(UserInterface, Timestamped, Base):
    COMPANY_ID: Final[int] = 10000000  # and greater
    DRIVER_ID: Final[int] = -1000  # and lower

    id: Final[Column[int]] = Column(
        'Id',
        Integer,
        primary_key=True,
        autoincrement=True,
        key='id',
    )

    @hybrid_property
    def is_company(self: Self, /) -> bool:
        return self.id >= self.COMPANY_ID

    @is_company.expression
    def is_company(cls: Type[Self], /) -> ClauseElement:
        return cls.id >= literal_column(str(cls.COMPANY_ID))

    @hybrid_property
    def is_person(self: Self, /) -> bool:
        return self.COMPANY_ID > self.id > 0

    @is_person.expression
    def is_person(cls: Type[Self], /) -> ClauseElement:
        return and_(
            literal_column(str(cls.COMPANY_ID)) > cls.id,
            cls.id > literal_column('0'),
        )

    @hybrid_property
    def is_service(self: Self, /) -> bool:
        return self.DRIVER_ID < self.id < 0

    @is_service.expression
    def is_service(cls: Type[Self], /) -> ClauseElement:
        return and_(
            literal_column(str(cls.DRIVER_ID)) < cls.id,
            cls.id < literal_column('0'),
        )

    @hybrid_property
    def is_driver(self: Self, /) -> bool:
        return self.id <= self.DRIVER_ID

    @is_driver.expression
    def is_driver(cls: Type[Self], /) -> ClauseElement:
        return cls.id <= literal_column(str(cls.DRIVER_ID))

    locales: Final[
        'RelationshipProperty[list[UserLocaleModel]]'
    ] = relationship(
        'UserLocaleModel',
        back_populates='user',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    deals: Final['RelationshipProperty[list[DealModel]]'] = relationship(
        'DealModel',
        back_populates='owner',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    active_deal: Final['RelationshipProperty[DealModel]'] = relationship(
        'DealModel',
        back_populates='owner',
        lazy='noload',
        primaryjoin='and_(DealModel.is_active, '
        'UserModel.id == DealModel.owner_id)',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=False,
        overlaps='deals',
    )
    company: Final['RelationshipProperty[CompanyModel]'] = relationship(
        'CompanyModel',
        back_populates='user',
        lazy='noload',
        primaryjoin='and_(UserModel.is_company, '
        'UserModel.id == CompanyModel.registry_number)',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=False,
    )
    person: Final['RelationshipProperty[PersonModel]'] = relationship(
        'PersonModel',
        back_populates='user',
        lazy='noload',
        primaryjoin='and_(UserModel.is_person, '
        'UserModel.id == PersonModel.user_id)',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=False,
    )
    group: Final['RelationshipProperty[GroupModel]'] = relationship(
        'GroupModel',
        back_populates='owner',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=False,
    )
    bonuses: Final['RelationshipProperty[list[BonusModel]]'] = relationship(
        'BonusModel',
        back_populates='owner',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    containers: Final[
        'RelationshipProperty[list[ContainerModel]]'
    ] = relationship(
        'ContainerModel',
        back_populates='owner',
        lazy='noload',
        primaryjoin='and_(UserModel.is_company, '
        'UserModel.id == ContainerModel.owner_id)',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    openings: Final[
        'RelationshipProperty[list[ContainerTankOpeningModel]]'
    ] = relationship(
        'ContainerTankOpeningModel',
        back_populates='user',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    clearings: Final[
        'RelationshipProperty[list[ContainerTankClearingModel]]'
    ] = relationship(
        'ContainerTankClearingModel',
        back_populates='user',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
