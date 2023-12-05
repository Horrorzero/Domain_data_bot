from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class User(Base):
	__tablename__ = 'user'

	id: Mapped[int] = mapped_column(primary_key=True)

	tg_id: Mapped[int] = mapped_column(Integer, unique=True)
	username: Mapped[str] = mapped_column(String, unique=True)

	domains: Mapped[list[Domain]] = relationship(
		back_populates='user',
		cascade='all, delete-orphan'
	)

	def __str__(self):
		return f'User:{self.username}'

	
class Domain(Base):
	__tablename__ = 'domain'

	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(String, unique=True)

	user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
	user: Mapped[User] = relationship(back_populates='domains')

	def __str__(self):
		return f'User:{self.name}'