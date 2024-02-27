from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.permission.models import Permission
from src.shared.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login: Mapped[str] = mapped_column(
        String(length=255), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(length=100), nullable=False)

    projects: Mapped[list["Permission"]] = relationship(back_populates="user")
