from src.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from sqlalchemy import String




class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column( nullable=False)
    

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"