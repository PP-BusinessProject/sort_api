# from datetime import datetime
# from decimal import Decimal
# from typing import TYPE_CHECKING, Final, Optional

# from sqlalchemy.orm import relationship
# from sqlalchemy.orm.relationships import RelationshipProperty
# from sqlalchemy.sql.schema import Column, ForeignKey
# from sqlalchemy.sql.sqltypes import Boolean, Integer, Numeric, DateTime

# from .._mixins import Timestamped
# from ..base_interface import Base
# from ..clients.user_model import UserModel
# from ..misc.addresses.address_model import AddressModel

# if TYPE_CHECKING:
#     from .delivery_nomenclature_model import DeliveryNomenclatureModel


# class DeliveryModel(Timestamped, Base):

#     id: Final[Column[int]] = Column(
#         Integer,
#         primary_key=True,
#         autoincrement=True,
#     )
#     user_id: Final[Column[int]] = Column(
#         UserModel.id.type,
#         ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='NO ACTION'),
#         nullable=False,
#     )
#     driver_id: Final[Column[Optional[int]]] = Column(
#         UserModel.id.type,
#         ForeignKey(UserModel.id, onupdate='CASCADE', ondelete='NO ACTION'),
#     )
#     latitude: Final[Column[Decimal]] = Column(
#         Numeric(8, 6),
#         nullable=False,
#     )
#     longtitude: Final[Column[Decimal]] = Column(
#         Numeric(9, 6),
#         nullable=False,
#     )
#     address_id: Final[Column[Optional[int]]] = Column(
#         AddressModel.id.type,
#         ForeignKey(AddressModel.id, onupdate='CASCADE', ondelete='RESTRICT'),
#     )
#     timestamp: Final[Column[Optional[datetime]]] = Column(
#         DateTime(timezone=True),
#     )
#     success: Final[Column[Optional[bool]]] = Column(
#         Boolean(create_constraint=True),
#     )

#     address: Final['RelationshipProperty[AddressModel]'] = relationship(
#         'AddressModel',
#         back_populates='deliveries',
#         lazy='noload',
#         cascade='save-update',
#         uselist=False,
#     )
#     nomenclatures: Final[
#         'RelationshipProperty[list[DeliveryNomenclatureModel]]'
#     ] = relationship(
#         'DeliveryNomenclatureModel',
#         back_populates='delivery',
#         lazy='noload',
#         cascade='save-update, merge, expunge, delete, delete-orphan',
#         uselist=True,
#     )
