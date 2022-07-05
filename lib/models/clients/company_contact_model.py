from enum import IntEnum, auto, unique
from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Enum, Integer

from ..base_interface import Base
from ..user_interface import UserInterface
from .company_model import CompanyModel


@unique
class ContactType(IntEnum):
    DIRECTOR: Final[int] = auto()
    ACCOUNTANT: Final[int] = auto()
    MANAGER: Final[int] = auto()


class CompanyContactModel(UserInterface, Base):
    company_registry_number: Final[Column[int]] = Column(
        'CompanyRegistryNumber',
        CompanyModel.registry_number.type,
        ForeignKey(
            CompanyModel.registry_number,
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        nullable=False,
        key='company_registry_number',
    )
    id: Final[Column[int]] = Column(
        'Id',
        Integer,
        primary_key=True,
        autoincrement=True,
        key='id',
    )
    type: Final[Column[ContactType]] = Column(
        'Type',
        Enum(ContactType, create_constraint=True),
        nullable=False,
        default=ContactType.DIRECTOR,
        key='type',
    )

    company: Final['RelationshipProperty[CompanyModel]'] = relationship(
        'CompanyModel',
        back_populates='contacts',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
