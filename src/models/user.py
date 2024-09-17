from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from app.database import Base
from sqlalchemy import Integer, String


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)

    transactions = relationship("Transaction", back_populates="user")

    def __repr__(self):
        return f"user id {self.id}"
