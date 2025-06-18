from sqlmodel import SQLModel, Field, func, Relationship
from datetime import datetime 
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
  from app.models.ItemApp import ItemApp

class Jenis(SQLModel, table=True):
  __tablename__ = "jenis"

  id: int|None = Field(primary_key=True, default=None)
  nama: str = Field(max_length=50)

  created_at: datetime = Field(default_factory=datetime.utcnow)
  updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": func.now()})

  # relationship
  items: List["ItemApp"] = Relationship(back_populates="jenis")