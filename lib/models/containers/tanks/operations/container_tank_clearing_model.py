# from typing import Any, Dict, Final, Tuple, Union

# from sqlalchemy.orm import relationship
# from sqlalchemy.orm.relationships import RelationshipProperty
# from sqlalchemy.sql.schema import (
#     Column,
#     ForeignKey,
#     ForeignKeyConstraint,
#     SchemaItem,
# )
# from sqlalchemy.sql.sqltypes import Integer

# from ...._mixins import Timestamped
# from ....base_interface import Base
# from ....clients.user_model import UserModel
# from ..container_tank_model import ContainerTankModel


# class ContainerTankClearingModel(Timestamped, Base):
#     user_id: Final[Column[int]] = Column(
#         UserModel.id.type,
#         ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='NO ACTION'),
#         nullable=False,
#     )
#     container_id: Final[Column[int]] = Column(
#         ContainerTankModel.container_id.type,
#         nullable=False,
#     )
#     tank_type_id: Final[Column[int]] = Column(
#         ContainerTankModel.type_id.type,
#         nullable=False,
#     )

#     id: Final[Column[int]] = Column(
#         Integer,
#         primary_key=True,
#         autoincrement=True,
#     )
#     volume: Final[Column[int]] = Column(
#         Integer,
#         nullable=False,
#     )

#     user: Final['RelationshipProperty[UserModel]'] = relationship(
#         'UserModel',
#         back_populates='clearings',
#         lazy='noload',
#         cascade='save-update',
#         uselist=False,
#     )
#     tank: Final['RelationshipProperty[ContainerTankModel]'] = relationship(
#         'ContainerTankModel',
#         back_populates='clearings',
#         lazy='noload',
#         cascade='save-update',
#         uselist=False,
#     )

#     __table_args__: Final[Tuple[Union[SchemaItem, Dict[str, Any]]]] = (
#         ForeignKeyConstraint(
#             [container_id, tank_type_id],
#             [ContainerTankModel.container_id, ContainerTankModel.type_id],
#             onupdate='CASCADE',
#             ondelete='NO ACTION',
#         ),
#     )
