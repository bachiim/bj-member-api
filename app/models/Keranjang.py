from sqlmodel import SQLModel, Field, func, Relationship
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from app.models.ItemApp import ItemApp
  from app.models.Satuan import Satuan

class Keranjang(SQLModel, table=True):
  __tablename__ = "keranjang"

  id: int|None = Field(primary_key=True, default=None)
  id_member: int = Field(foreign_key="members.id")
  id_item: str = Field(foreign_key="items.id")
  id_satuan: int = Field(foreign_key="satuan.id")
  jumlah: int = Field()

  created_at: datetime = Field(default_factory=datetime.utcnow)
  updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": func.now()})

  # relationship
  item: "ItemApp" = Relationship(back_populates="keranjang")
  satuan: "Satuan" = Relationship(back_populates="keranjang")