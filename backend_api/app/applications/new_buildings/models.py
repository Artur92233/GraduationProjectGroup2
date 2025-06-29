import uuid
from datetime import datetime

from database.base_models import Base
from sqlalchemy import ARRAY, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column


class NewBuildings(Base):
    __tablename__ = "new_buildings"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    uuid_data: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4)

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(String(200), nullable=False)
    contact: Mapped[str] = mapped_column(String(100), nullable=False)
    main_image: Mapped[str] = mapped_column(nullable=False)
    images: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)

    def __str__(self):
        return f"{self.type.capitalize()} - {self.title} ({self.id})"
