# from decimal import Decimal
# from typing import Final

# from sqlalchemy.orm import relationship
# from sqlalchemy.orm.relationships import RelationshipProperty
# from sqlalchemy.sql.schema import CheckConstraint, Column, ForeignKey
# from sqlalchemy.sql.sqltypes import Numeric

# from .._mixins import Timestamped
# from ..base_interface import Base
# from ..nomenclatures.nomenclature_model import NomenclatureModel
# from .delivery_model import DeliveryModel


# class DeliveryNomenclatureModel(Timestamped, Base):
#     delivery_id: Final[Column[int]] = Column(
#         DeliveryModel.id.type,
#         ForeignKey(DeliveryModel.id, onupdate='CASCADE', ondelete='CASCADE'),
#         primary_key=True,
#     )
#     nomenclature_id: Final[Column[int]] = Column(
#         NomenclatureModel.id.type,
#         ForeignKey(
#             NomenclatureModel.id,
#             onupdate='CASCADE',
#             ondelete='RESTRICT',
#         ),
#         primary_key=True,
#     )
#     amount: Final[Column[Decimal]] = Column(
#         Numeric,
#         CheckConstraint('amount > 0'),
#         nullable=False,
#         default=1,
#     )

#     delivery: Final[
#         'RelationshipProperty[list[DeliveryModel]]'
#     ] = relationship(
#         'DeliveryModel',
#         back_populates='nomenclatures',
#         lazy='noload',
#         cascade='save-update',
#         uselist=False,
#     )
#     nomenclature: Final[
#         'RelationshipProperty[list[NomenclatureModel]]'
#     ] = relationship(
#         'NomenclatureModel',
#         lazy='noload',
#         cascade='save-update',
#         uselist=False,
#     )
