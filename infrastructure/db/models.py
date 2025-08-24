from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Text, UniqueConstraint
from typing import List, Optional

class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)

    notes: Mapped[List["NoteModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    groups: Mapped[List["GroupModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

class GroupModel(Base):
    __tablename__ = "groups"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_group_user_name"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)

    user: Mapped["UserModel"] = relationship(back_populates="groups")
    notes: Mapped[List["NoteModel"]] = relationship(back_populates="group")

class NoteModel(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    group_id: Mapped[Optional[int]] = mapped_column(ForeignKey("groups.id"), nullable=True, index=True)

    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    color_hex: Mapped[Optional[str]] = mapped_column(String(7), nullable=True)  # "#RRGGBB"
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user: Mapped["UserModel"] = relationship(back_populates="notes")
    group: Mapped[Optional["GroupModel"]] = relationship(back_populates="notes")
