from sqlmodel import SQLModel, Field, Text, func, Relationship
from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
  from app.models.Member import Member

class Sales(SQLModel, table=True):
  __tablename__ = "sales"

  id: int|None = Field(primary_key=True, default=None)
  nama: str = Field(max_length=100)
  alamat: str = Field(sa_type=Text)
  telepon: str = Field(max_length=12, unique=True)

  created_at: datetime = Field(default_factory=datetime.utcnow)
  updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": func.now()})
  # member relationship
  members: List["Member"] = Relationship(back_populates="sales")