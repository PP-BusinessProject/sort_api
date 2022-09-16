"""The module that provides a `JuridicalPersonModel`."""


from typing import TYPE_CHECKING, Final, Optional
from uuid import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

from ..auth.user_model import UserModel
from ..base_interface import Base
from ..misc.addresses.address_model import AddressModel
from ..misc.banks.bank_model import BankModel

if TYPE_CHECKING:
    from ..containers.container_model import ContainerModel
    from .bonuses.company_bonus_model import CompanyBonusModel
    from .company_image_model import CompanyImageModel
    from .company_locale_model import CompanyLocaleModel
    from .contacts.company_contact_model import CompanyContactModel
    from .deals.company_deal_model import CompanyDealModel
    from .groups.company_group_model import CompanyGroupModel


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

    user_id: Final[Column[UUID]] = Column(
        UserModel.id.type,
        ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
    )
    registry_number: Final[Column[int]] = Column(
        Integer,
        unique=True,
        nullable=False,
    )
    fallback_name: Final[Column[str]] = Column(
        String(64),
        CheckConstraint("fallback_name <> ''"),
        nullable=False,
    )
    tax_number: Final[Column[Optional[int]]] = Column(Integer)
    address_id: Final[Column[int]] = Column(
        AddressModel.id.type,
        ForeignKey(AddressModel.id, onupdate='CASCADE', ondelete='RESTRICT'),
        nullable=False,
    )
    real_address_id: Final[Column[Optional[int]]] = Column(
        AddressModel.id.type,
        ForeignKey(AddressModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        CheckConstraint('real_address_id <> address_id'),
    )
    bank_code: Final[Column[int]] = Column(
        BankModel.code.type,
        ForeignKey(BankModel.code, onupdate='CASCADE', ondelete='RESTRICT'),
        nullable=False,
    )
    bank_account_number: Final[Column[str]] = Column(
        String(29),
        CheckConstraint("bank_account_number <> ''"),
        nullable=False,
    )

    locales: Final[
        'RelationshipProperty[list[CompanyLocaleModel]]'
    ] = relationship(
        'CompanyLocaleModel',
        back_populates='company',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    images: Final[
        'RelationshipProperty[list[CompanyImageModel]]'
    ] = relationship(
        'CompanyImageModel',
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
    bank: Final['RelationshipProperty[BankModel]'] = relationship(
        'BankModel',
        back_populates='companies',
        lazy='noload',
        cascade='save-update',
        uselist=False,
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
    deals: Final[
        'RelationshipProperty[list[CompanyDealModel]]'
    ] = relationship(
        'CompanyDealModel',
        back_populates='company',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    group: Final[
        'RelationshipProperty[Optional[CompanyGroupModel]]'
    ] = relationship(
        'CompanyGroupModel',
        back_populates='owner',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    bonuses: Final[
        'RelationshipProperty[list[CompanyBonusModel]]'
    ] = relationship(
        'CompanyBonusModel',
        back_populates='company',
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
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
