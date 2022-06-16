"""Custom column types for the mapped classes."""

from datetime import datetime, timedelta, tzinfo
from enum import Enum
from importlib import import_module
from inspect import isfunction
from numbers import Number
from types import ModuleType
from typing import Any, Final, Generic, Optional, Type, TypeVar, Union

from dateutil.tz.tz import tzlocal
from sqlalchemy.sql.sqltypes import Float, Integer, String
from sqlalchemy.sql.type_api import TypeDecorator, TypeEngine
from typing_extensions import Self

#
_Enum = TypeVar('_Enum', bound=Enum, covariant=True)


class IntEnumType(TypeDecorator[_Enum], Generic[_Enum]):
    """The type for storing a enum in the database as integer."""

    impl: Union[Type[TypeEngine[Any]], TypeEngine[Any]] = Integer
    cache_ok: Final[bool] = True

    _enumtype: Final[Type[_Enum]]

    def __init__(
        self,
        enumtype: Type[_Enum],
        /,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize this enum."""
        super().__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(
        self: Self,
        value: Optional[Any],
        dialect: Any,
        /,
    ) -> Optional[int]:
        """Return enum value."""
        return value.value if isinstance(value, Enum) else None

    def process_result_value(
        self: Self,
        value: Optional[Any],
        dialect: Any,
        /,
    ) -> Optional[_Enum]:
        """Bind the enum from value."""
        return self._enumtype(value)


class DateTimeISO8601(TypeDecorator[datetime]):
    """The type for storing a enum in the database as integer."""

    impl: Union[Type[TypeEngine[Any]], TypeEngine[Any]] = String(32)
    cache_ok: Final[bool] = False

    sep: Final[str]
    timespec: Final[str]
    default_timezone: Final[tzinfo]
    timezone: Final[tzinfo]

    def __init__(
        self,
        /,
        sep: str = 'T',
        timespec: str = 'auto',
        default_timezone: tzinfo = tzlocal(),
        timezone: tzinfo = tzlocal(),
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize this enum."""
        super().__init__(*args, **kwargs)
        self.sep, self.timespec = sep, timespec
        self.default_timezone, self.timezone = default_timezone, timezone

    def process_bind_param(
        self: Self,
        value: Optional[Any],
        dialect: Any,
        /,
    ) -> Optional[str]:
        """Return ISO8601 formatted string from datetime `value`."""
        if isinstance(value, datetime):
            if value.tzinfo is None:
                value = value.replace(tzinfo=self.default_timezone)
            return value.isoformat(sep=self.sep, timespec=self.timespec)
        return None

    def process_result_value(
        self: Self,
        value: Optional[Any],
        dialect: Any,
        /,
    ) -> Optional[datetime]:
        """Return the datetime from the ISO8601 formatted string `value`."""
        if isinstance(value, str):
            return datetime.fromisoformat(value).astimezone(self.timezone)
        return None


class TimeDelta(TypeDecorator[timedelta]):
    """The type for storing a timedelta in the database as float."""

    impl: Union[Type[TypeEngine[Any]], TypeEngine[Any]] = Float(25)
    cache_ok: Final[bool] = True

    def process_bind_param(
        self: Self,
        value: Optional[Any],
        dialect: Any,
        /,
    ) -> Optional[float]:
        """Return timdelta's total seconds."""
        return value.total_seconds() if isinstance(value, timedelta) else None

    def process_result_value(
        self: Self,
        value: Optional[Any],
        dialect: Any,
        /,
    ) -> Optional[timedelta]:
        """Bind the enum from value."""
        return timedelta(seconds=value) if isinstance(value, Number) else None


class LocalFunction(TypeDecorator):
    """The SQLAlchemy converter for the `CategoryModel`."""

    impl: Union[Type[TypeEngine], TypeEngine] = String
    cache_ok: bool = False

    def process_bind_param(
        self: Self,
        value: Optional[Any],
        /,
        dialect: Any = None,
    ) -> Optional[str]:
        """Return enum value."""
        if isfunction(value):
            return ':'.join((value.__module__, value.__qualname__))
        return None

    def process_result_value(
        self: Self,
        value: Optional[Any],
        /,
        dialect: Any = None,
    ) -> Optional[ModuleType]:
        """Bind the enum from value."""
        if not isinstance(value, str):
            return None

        module, _, name = value.rpartition(':')
        if not (module and name):
            return None

        try:
            class_, _, name = name.partition('.')
            obj = getattr(import_module(module), class_)
            while name:
                temp = name.partition('.')
                obj = getattr(obj, temp[0])
                class_, _, name = temp
            return obj if isfunction(obj) else None
        except (AttributeError, ImportError):
            return None
