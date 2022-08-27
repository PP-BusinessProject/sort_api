from typing import Final

from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
from sqlalchemy.sql.sqltypes import String

from ..._mixins import Timestamped
from ...base_interface import Base
from ...misc.locales.locale_model import LocaleModel
from .group_right_model import GroupRightModel


class GroupRightLocaleModel(Timestamped, Base):
    right_id: Final[Column[int]] = Column(
        'RightId',
        GroupRightModel.id.type,
        ForeignKey(GroupRightModel.id, onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
        key='type_id',
    )
    locale_alpha_2: Final[Column[str]] = Column(
        'LocaleAlpha2',
        LocaleModel.alpha_2.type,
        ForeignKey(
            LocaleModel.alpha_2,
            onupdate='CASCADE',
            ondelete='RESTRICT',
        ),
        primary_key=True,
        key='locale_alpha_2',
    )

    name: Final[Column[str]] = Column(
        'Name',
        String(255),
        CheckConstraint('"Name" <> \'\''),
        nullable=False,
        key='name',
    )

    locale: Final['RelationshipProperty[LocaleModel]'] = relationship(
        'LocaleModel',
        back_populates='group_right_locales',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
    right: Final['RelationshipProperty[GroupRightModel]'] = relationship(
        'GroupRightModel',
        back_populates='locales',
        lazy='noload',
        cascade='save-update',
        uselist=False,
    )
