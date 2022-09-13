from typing import Any, Dict, Final, Iterable, Tuple, Type, Union

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.elements import ClauseElement
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import (
    CheckConstraint,
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    SchemaItem,
)
from sqlalchemy.sql.sqltypes import String
from typing_extensions import Self

from .._mixins import Timestamped
from ..base_interface import Base
from ..misc.locales.locale_model import LocaleModel
from .user_model import UserModel


class UserLocaleModel(Timestamped, Base):
    user_id: Final[Column[int]] = Column(
        UserModel.id.type,
        ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
    )
    locale_language_code: Final[Column[str]] = Column(
        LocaleModel.language_code.type,
        primary_key=True,
    )
    locale_country_code: Final[Column[str]] = Column(
        LocaleModel.country_code.type,
        primary_key=True,
    )

    first_name: Final[Column[str]] = Column(
        String(64),
        CheckConstraint("first_name <> ''"),
        nullable=False,
    )
    last_name: Final[Column[str]] = Column(
        String(64),
        nullable=False,
        default='',
    )

    locale: Final['RelationshipProperty[LocaleModel]'] = relationship(
        'LocaleModel',
        back_populates='user_locales',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    user: Final['RelationshipProperty[UserModel]'] = relationship(
        'UserModel',
        back_populates='locales',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )

    @hybrid_property
    def full_name(self: Self, /) -> str:
        """Return the name of this user."""
        return ' '.join(_ for _ in (self.first_name, self.last_name) if _)

    @full_name.setter
    def full_name(self: Self, value: str, /) -> None:
        if not value:
            raise ValueError('value is empty.')
        self.first_name, self.last_name, *_ = (value.split(' ', 1), '')

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

    __table_args__: Final[Tuple[Union[SchemaItem, Dict[str, Any]]]] = (
        ForeignKeyConstraint(
            [locale_language_code, locale_country_code],
            [LocaleModel.language_code, LocaleModel.country_code],
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
    )
