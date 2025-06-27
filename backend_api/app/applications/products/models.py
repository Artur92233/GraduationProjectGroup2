import uuid
from datetime import datetime

from sqlalchemy import func, String, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from database.base_models import Base


class Products(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    uuid_data: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4)

    title: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(1000), index=True, default="")
    price: Mapped[float] = mapped_column(nullable=False)
    main_image: Mapped[str] = mapped_column(nullable=False)
    images: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)

    def __str__(self):
        return f'Product {self.title} - {self.id}'