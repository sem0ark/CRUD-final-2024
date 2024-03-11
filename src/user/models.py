from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

import src.project.models
from src.shared.database import Base
from src.shared.models import BaseTimestamp


class User(Base, BaseTimestamp):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    login: Mapped[str] = mapped_column(
        String(length=255), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(length=100), nullable=False)

    projects: Mapped[list["src.project.models.Permission"]] = relationship(
        back_populates="user"
    )

    def __str__(self):
        return f"UserModel[{self.id}; {self.login}]"

    def __repr__(self):
        return self.__str__()
