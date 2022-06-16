from typing import Iterable, Optional, Type

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.decl_api import declared_attr
from sqlalchemy.sql.elements import ClauseElement
from sqlalchemy.sql.expression import func
from sqlalchemy.sql.schema import CheckConstraint, Column
from sqlalchemy.sql.sqltypes import String
from sqlalchemy_utils.types.email import EmailType
from sqlalchemy_utils.types.phone_number import PhoneNumber, PhoneNumberType
from typing_extensions import Self

from .base_interface import BaseInterface


class UserInterface(BaseInterface):
    @declared_attr
    def first_name(self: Self, /) -> Column[str]:
        return Column(
            'FirstName',
            String(64),
            CheckConstraint('"FirstName" <> \'\''),
            nullable=False,
            key='first_name',
        )

    @declared_attr
    def last_name(self: Self, /) -> Column[Optional[str]]:
        return Column(
            'LastName',
            String(64),
            CheckConstraint('"LastName" <> \'\''),
            key='last_name',
        )

    @declared_attr
    def phone_number(self: Self, /) -> Column[PhoneNumber]:
        return Column(
            'PhoneNumber',
            PhoneNumberType('UA', 20),
            index=True,
            unique=True,
            nullable=False,
            key='phone_number',
        )

    @declared_attr
    def email(self: Self, /) -> Column[Optional[str]]:
        return Column(
            'Email',
            EmailType,
            index=True,
            unique=True,
            key='email',
        )

    @hybrid_property
    def full_name(self: Self, /) -> str:
        """Return the name of this user."""
        return ' '.join(_ for _ in (self.first_name, self.last_name) if _)

    @full_name.setter
    def full_name(self: Self, value: str, /) -> None:
        if not value:
            raise ValueError('value is empty.')
        self.first_name, self.last_name, *_ = value.split(' ', 1), ''

    @full_name.expression
    def full_name(cls: Type[Self], /) -> ClauseElement:
        last_name_check = func.nullif(cls.last_name, '')
        return func.concat_ws(' ', cls.first_name, last_name_check)

    @full_name.update_expression
    def full_name(
        cls: Type[Self],
        value: str,
        /,
    ) -> Iterable[tuple[Column, str]]:
        if not value:
            raise ValueError('value is empty.')
        first_name, last_name, *_ = value.split(' ', 1), ''
        return [(cls.first_name, first_name), (cls.last_name, last_name)]
