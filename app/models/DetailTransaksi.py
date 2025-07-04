from sqlmodel import SQLModel, Field, func, Relationship
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from .Transaksi import Transaksi
  from .Satuan import Satuan
  from .ItemApp import ItemApp

class DetailTransaksi(SQLModel, table=True):
  __tablename__ = "detail_transaksi"

  id: int = Field(primary_key=True, default=None)
  id_transaksi: int = Field(foreign_key="transaksi.id")
  id_item: str = Field(foreign_key="items.id")
  id_satuan: int = Field(foreign_key="satuan.id")
  jumlah: int = Field()
  harga: int = Field()
  subtotal: int = Field()

  created_at: datetime = Field(default_factory=datetime.utcnow)
  updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": func.now()})

  # relationship
  transaksi: "Transaksi" = Relationship(back_populates="details")
  item: "ItemApp" = Relationship(back_populates="detail_transaksi")
  satuan: "Satuan" = Relationship(back_populates="detail_transaksi")