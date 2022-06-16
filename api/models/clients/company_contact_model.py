from enum import IntEnum, auto
from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from .._types import IntEnumType
from ..base_interface import Base
from ..user_interface import UserInterface
from .company_model import CompanyModel


class ContactType(IntEnum):
    DIRECTOR: Final[int] = auto()
    ACCOUNTANT: Final[int] = auto()
    MANAGER: Final[int] = auto()


class CompanyContactModel(UserInterface, Base):
    company_id: Final[Column[int]] = Column(
        'CompanyId',
        CompanyModel.id.type,
        ForeignKey(CompanyModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
        key='company_id',
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
        IntEnumType(ContactType),
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
