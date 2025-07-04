from sqlmodel import SQLModel, Field, func, Relationship
from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
  from app.models.Member import Member

class Level(SQLModel, table=True):
  __tablename__ = "levels"

  id: int|None = Field(primary_key=True, default=None)
  nama: str = Field(max_length=50)
  potongan: float = Field()

  created_at: datetime = Field(default_factory=datetime.utcnow)
  updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": func.now()})

  # relationship
  members: List["Member"] = Relationship(back_populates="level")