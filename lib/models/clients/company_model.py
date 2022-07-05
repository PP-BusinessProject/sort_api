"""The module that provides a `JuridicalPersonModel`."""


from typing import TYPE_CHECKING, Final, Optional

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.expression import literal_column
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from ..base_interface import Base
from ..misc.address_model import AddressModel
from ..misc.bank_model import BankModel
from .user_model import UserModel

if TYPE_CHECKING:
    from .company_contact_model import CompanyContactModel


class CompanyModel(Base):
    """
    The model that represents a juridical person.

    Parameters:
        id (``int``):
            The id of this juridical person in the database.

        created_at (``datetime``):
            The date and time this model was added to the database.

        updated_at (``datetime``):
            The date and time of the last time this model was updated in the
            database.
    """

    registry_number: Final[Column[int]] = Column(
        'RegistryNumber',
        UserModel.id.type,
        ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        CheckConstraint(
            literal_column('"RegistryNumber"')
            >= literal_column(str(UserModel.COMPANY_ID))
        ),
        primary_key=True,
        key='registry_number',
    )
    tax_number: Final[Column[Optional[int]]] = Column(
        'TaxNumber',
        Integer,
        key='tax_number',
    )
    address_id: Final[Column[int]] = Column(
        'AddressId',
        AddressModel.id.type,
        ForeignKey(AddressModel.id, onupdate='CASCADE', ondelete='RESTRICT'),
        nullable=False,
        key='address_id',
    )
    real_address_id: Final[Column[Optional[int]]] = Column(
        'RealAddressId',
        AddressModel.id.type,
        ForeignKey(AddressModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        CheckConstraint('"RealAddressId" <> "AddressId"'),
        key='real_address_id',
    )
    bank_code: Final[Column[int]] = Column(
        'BankCode',
        BankModel.code.type,
        ForeignKey(BankModel.code, onupdate='CASCADE', ondelete='RESTRICT'),
        nullable=False,
        key='bank_code',
    )
    bank_account_number: Final[Column[str]] = Column(
        'BankAccountNumber',
        String(29),
        nullable=False,
        key='bank_account_number',
    )

    bank: Final['RelationshipProperty[BankModel]'] = relationship(
        'BankModel',
        back_populates='companies',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    address: Final['RelationshipProperty[AddressModel]'] = relationship(
        'AddressModel',
        back_populates='companies',
        lazy='noload',
        primaryjoin=address_id == AddressModel.id,
        cascade='save-update',
        uselist=False,
    )
    real_address: Final[
        'RelationshipProperty[Optional[AddressModel]]'
    ] = relationship(
        'AddressModel',
        back_populates='companies',
        lazy='noload',
        primaryjoin=real_address_id == AddressModel.id,
        cascade='save-update',
        uselist=False,
        overlaps='address',
    )
    contacts: Final[
        'RelationshipProperty[list[CompanyContactModel]]'
    ] = relationship(
        'CompanyContactModel',
        back_populates='company',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    user: Final['RelationshipProperty[UserModel]'] = relationship(
        'UserModel',
        back_populates='company',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
