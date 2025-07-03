import uuid
from datetime import datetime
from email.policy import default

from database.base_models import Base
from sqlalchemy import ARRAY, String, Text, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ModalCommonMixin:
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())

class NewBuildings(ModalCommonMixin, Base):
    __tablename__ = "new_buildings"


    uuid_data: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4)

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    apartment_count: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(String(200), nullable=False)
    contact: Mapped[str] = mapped_column(String(100), nullable=False)
    main_image: Mapped[str] = mapped_column(nullable=False)
    images: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)

    selected_NewBuildings = relationship("SelectedNewBuildings", back_populates="NewBuilding", lazy="selectin")

    def __str__(self):
        return f"{self.type.capitalize()} - {self.title} ({self.id})"

# applications/new_buildings/models.py
class Selected(ModalCommonMixin, Base):
    __tablename__ = "selected"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_closed: Mapped[bool] = mapped_column(default=False)

    selected_NewBuildings = relationship("SelectedNewBuildings", back_populates="selected", lazy="selectin")

    @property
    def cost(self):
        return sum(selected_NewBuildings.total for selected_NewBuildings in self.selected_NewBuildings)

class SelectedNewBuildings(ModalCommonMixin, Base):
    __tablename__ = "selected_new_buildings"

    selected_id: Mapped[int] = mapped_column(ForeignKey("selected.id"))
    NewBuildings_id: Mapped[int] = mapped_column(ForeignKey("new_buildings.id"))
    price: Mapped[float] = mapped_column(default=0.0)
    quantity: Mapped[float] = mapped_column(default=0.0)

    selected = relationship("Selected", back_populates="selected_NewBuildings", lazy="selectin")
    NewBuilding = relationship("NewBuildings", back_populates="selected_NewBuildings", lazy="selectin")

    @property
    def total(self) -> float:
        return self.price * self.quantity
