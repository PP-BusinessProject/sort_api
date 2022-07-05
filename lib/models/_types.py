"""Custom column types for the mapped classes."""


from typing import Any, Callable, Final, Iterable, Type, Union

from sqlalchemy import Unicode
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.properties import ColumnProperty
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.type_api import TypeDecorator, TypeEngine
from typing_extensions import Self


def inspect_type(mixed):
    if isinstance(mixed, InstrumentedAttribute):
        return mixed.property.columns[0].type
    elif isinstance(mixed, ColumnProperty):
        return mixed.columns[0].type
    elif isinstance(mixed, Column):
        return mixed.type


def is_case_insensitive(mixed):
    try:
        return isinstance(
            inspect_type(mixed).comparator, CaseInsensitiveComparator
        )
    except AttributeError:
        try:
            return issubclass(
                inspect_type(mixed).comparator_factory,
                CaseInsensitiveComparator,
            )
        except AttributeError:
            return False


class CaseInsensitiveComparator(Unicode.Comparator):
    @classmethod
    def lowercase_arg(cls: Type[Self], /, function: str) -> Callable:
        def operation(self: Self, /, other, **kwargs: Any) -> Callable:
            operator = getattr(Unicode.Comparator, function)
            if other is None:
                return operator(self, other, **kwargs)
            if not is_case_insensitive(other):
                other = func.lower(other)
            return operator(self, other, **kwargs)

        return operation

    def in_(self, other):
        if isinstance(other, Iterable):
            other = map(func.lower, other)
        return Unicode.Comparator.in_(self, other)

    def notin_(self, other):
        if isinstance(other, Iterable):
            other = map(func.lower, other)
        return Unicode.Comparator.notin_(self, other)


class CaseInsensitiveUnicode(TypeDecorator):
    impl: Final[Union[Type[TypeEngine], TypeEngine]] = Unicode
    comparator_factory: Final[Any] = CaseInsensitiveComparator
    cache_ok: Final[bool] = True

    def __init__(
        self: Self,
        length: int = 255,
        *args: Any,
        **kwargs: Any,
    ):
        super(CaseInsensitiveUnicode, self).__init__(
            length=length, *args, **kwargs
        )

    @property
    def python_type(self: Self, /) -> Type[Any]:
        return self.impl.type.python_type
