from datetime import date
from typing import Iterable, Optional, Type

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.decl_api import declared_attr
from sqlalchemy.sql.elements import ClauseElement
from sqlalchemy.sql.expression import func
from sqlalchemy.sql.schema import CheckConstraint, Column
from sqlalchemy.sql.sqltypes import BigInteger, Date, String
from typing_extensions import Self

from ._types import CaseInsensitiveUnicode
from .base_interface import BaseInterface


class UserInterface(BaseInterface):
    @declared_attr
    def fallback_first_name(self: Self, /) -> Column[str]:
        return Column(
            'FallbackFirstName',
            String(64),
            CheckConstraint('"FallbackFirstName" <> \'\''),
            nullable=False,
            key='fallback_first_name',
        )

    @declared_attr
    def fallback_last_name(self: Self, /) -> Column[str]:
        return Column(
            'FallbackLastName',
            String(64),
            nullable=False,
            default='',
            key='fallback_last_name',
        )

    @declared_attr
    def phone_number(self: Self, /) -> Column[int]:
        return Column(
            'PhoneNumber',
            BigInteger,
            index=True,
            unique=True,
            nullable=False,
            key='phone_number',
        )

    @declared_attr
    def email(self: Self, /) -> Column[Optional[str]]:
        return Column(
            'Email',
            CaseInsensitiveUnicode,
            index=True,
            unique=True,
            key='email',
        )

    @declared_attr
    def birthday(self: Self, /) -> Column[Optional[date]]:
        return Column('Birthday', Date, key='birthday')

    @hybrid_property
    def fallback_full_name(self: Self, /) -> str:
        """Return the name of this user."""
        return ' '.join(
            _ for _ in (self.fallback_first_name, self.fallback_last_name) if _
        )

    @fallback_full_name.setter
    def fallback_full_name(self: Self, value: str, /) -> None:
        if not value:
            raise ValueError('value is empty.')
        self.fallback_first_name, self.fallback_last_name, *_ = (
            value.split(' ', 1),
            '',
        )

    @fallback_full_name.expression
    def fallback_full_name(cls: Type[Self], /) -> ClauseElement:
        last_name_check = func.nullif(cls.fallback_last_name, '')
        return func.concat_ws(' ', cls.fallback_first_name, last_name_check)

    @fallback_full_name.update_expression
    def fallback_full_name(
        cls: Type[Self],
        value: str,
        /,
    ) -> Iterable[tuple[Column, str]]:
        if not value:
            raise ValueError('value is empty.')
        first_name, last_name, *_ = value.split(' ', 1), ''
        return [
            (cls.fallback_first_name, first_name),
            (cls.fallback_last_name, last_name),
        ]
