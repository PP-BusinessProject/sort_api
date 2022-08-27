from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from ...base_interface import Base
from ...user_interface import UserInterface
from .company_contact_type_model import CompanyContactTypeModel
from .company_model import CompanyModel


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
    type_id: Final[Column[int]] = Column(
        'TypeId',
        CompanyContactTypeModel.id.type,
        ForeignKey(
            CompanyContactTypeModel.id,
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        nullable=False,
        key='type_id',
    )

    company: Final['RelationshipProperty[CompanyModel]'] = relationship(
        'CompanyModel',
        back_populates='contacts',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    type: Final[
        'RelationshipProperty[CompanyContactTypeModel]'
    ] = relationship(
        'CompanyContactTypeModel',
        back_populates='contacts',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
