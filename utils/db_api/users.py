from sqlalchemy import Column, Integer, BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column
from utils.db_api.base import Base
from typing import Optional



class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    status: Mapped[int] = mapped_column(Integer, default=0)
