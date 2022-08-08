"""The module with the mixins for the mapped classes."""

from datetime import datetime

from dateutil.tz.tz import tzlocal
from sqlalchemy.orm.decl_api import declared_attr
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DateTime
from typing_extensions import Self


class Timestamped(object):
    """The mixin for setting timestamps for the mapped classes."""

    @declared_attr
    def created_at(self: Self, /) -> Column[datetime]:
        """Set the date and time when the instance was created."""
        return Column(
            'CreatedAt',
            DateTime(timezone=True),
            nullable=False,
            default=lambda: datetime.now(tzlocal()),
            key='created_at',
        )

    @declared_attr
    def updated_at(self: Self, /) -> Column[datetime]:
        """Set the date and time of the last time the instance was updated."""
        return Column(
            'UpdatedAt',
            DateTime(timezone=True),
            nullable=False,
            default=lambda: datetime.now(tzlocal()),
            onupdate=lambda: datetime.now(tzlocal()),
            key='updated_at',
        )
