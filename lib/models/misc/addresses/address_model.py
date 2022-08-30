from __future__ import annotations

from typing import TYPE_CHECKING, Final, Type

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.elements import ClauseElement
from sqlalchemy.sql.schema import CheckConstraint, Column
from sqlalchemy.sql.sqltypes import Integer, SmallInteger, String
from typing_extensions import Self

from ...base_interface import Base

if TYPE_CHECKING:
    from ...clients.companies.company_model import CompanyModel
    from ...containers.container_model import ContainerModel
    from ...deliveries.delivery_model import DeliveryModel
    from ..banks.bank_model import BankModel
    from .address_locale_model import AddressLocaleModel


class AddressModel(Base):
    id: Final[Column[int]] = Column(
        'Id',
        Integer,
        primary_key=True,
        autoincrement=True,
        key='id',
    )
    fallback_country: Final[Column[str]] = Column(
        'FallbackСountry',
        String(255),
        CheckConstraint('"FallbackСountry" <> \'\''),
        nullable=False,
        default='Ukraine',
        key='fallback_country',
    )
    fallback_state: Final[Column[str]] = Column(
        'FallbackState',
        String(255),
        CheckConstraint('"FallbackState" <> \'\''),
        nullable=False,
        key='fallback_state',
    )
    fallback_city: Final[Column[str]] = Column(
        'FallbackCity',
        String(255),
        CheckConstraint('"FallbackCity" <> \'\''),
        nullable=False,
        key='fallback_city',
    )
    fallback_street: Final[Column[str]] = Column(
        'FallbackStreet',
        String(255),
        CheckConstraint('"FallbackStreet" <> \'\''),
        nullable=False,
        key='fallback_street',
    )
    building: Final[Column[int]] = Column(
        'Building',
        SmallInteger,
        nullable=False,
        key='building',
    )
    postal_code: Final[Column[int]] = Column(
        'PostalCode',
        Integer,
        nullable=False,
        key='postal_code',
    )

    @hybrid_property
    def full(self: Self, /) -> str:
        """Return the full address."""
        return ', '.join(
            str(_)
            for _ in (
                self.postal_code,
                self.country,
                self.state,
                self.city,
                self.street,
                self.building,
            )
            if _ is not None
        )

    @full.expression
    def full(cls: Type[Self], /) -> ClauseElement:
        # sourcery skip: instance-method-first-arg-name
        return (
            cls.postal_code.concat(', ')
            .concat(cls.country)
            .concat(', ')
            .concat(cls.state)
            .concat(', ')
            .concat(cls.city)
            .concat(', ')
            .concat(cls.street)
            .concat(', ')
            .concat(cls.building)
        )

    locales: Final[
        'RelationshipProperty[list[AddressLocaleModel]]'
    ] = relationship(
        'AddressLocaleModel',
        back_populates='address',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    banks: Final['RelationshipProperty[BankModel]'] = relationship(
        'BankModel',
        back_populates='address',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    companies: Final['RelationshipProperty[CompanyModel]'] = relationship(
        'CompanyModel',
        back_populates='address',
        lazy='noload',
        primaryjoin='AddressModel.id == CompanyModel.address_id',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    containers: Final['RelationshipProperty[ContainerModel]'] = relationship(
        'ContainerModel',
        back_populates='address',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
    deliveries: Final['RelationshipProperty[DeliveryModel]'] = relationship(
        'DeliveryModel',
        back_populates='address',
        lazy='noload',
        cascade='save-update, merge, expunge, delete, delete-orphan',
        uselist=True,
    )
