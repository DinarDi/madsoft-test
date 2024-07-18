from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from .base import Base


class Meme(Base):
    title: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(String(300))
    img_url: Mapped[str] = mapped_column(nullable=True, default=None)
