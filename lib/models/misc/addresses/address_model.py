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
    from ...companies.company_model import CompanyModel
    from ...containers.container_model import ContainerModel

    # from ...deliveries.delivery_model import DeliveryModel
    from ..banks.bank_model import BankModel
    from .address_locale_model import AddressLocaleModel


class AddressModel(Base):
    id: Final[Column[int]] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    fallback_country: Final[Column[str]] = Column(
        String(255),
        CheckConstraint("fallback_country <> ''"),
        nullable=False,
        default='Ukraine',
    )
    fallback_state: Final[Column[str]] = Column(
        String(255),
        CheckConstraint("fallback_state <> ''"),
        nullable=False,
    )
    fallback_city: Final[Column[str]] = Column(
        String(255),
        CheckConstraint("fallback_city <> ''"),
        nullable=False,
    )
    fallback_street: Final[Column[str]] = Column(
        String(255),
        CheckConstraint("fallback_street <> ''"),
        nullable=False,
    )
    building: Final[Column[int]] = Column(
        SmallInteger,
        nullable=False,
    )
    postal_code: Final[Column[int]] = Column(
        Integer,
        nullable=False,
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
    # deliveries: Final['RelationshipProperty[DeliveryModel]'] = relationship(
    #     'DeliveryModel',
    #     back_populates='address',
    #     lazy='noload',
    #     cascade='save-update, merge, expunge, delete, delete-orphan',
    #     uselist=True,
    # )
