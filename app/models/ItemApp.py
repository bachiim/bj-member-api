from sqlmodel import SQLModel, Field, func, Text, Relationship
from datetime import datetime
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
  from app.models.Keranjang import Keranjang
  from app.models.Jenis import Jenis
  from app.models.DetailTransaksi import DetailTransaksi

class ItemApp(SQLModel, table=True):
  __tablename__ = "items"

  id: str = Field(primary_key=True, max_length=100)
  nama: str = Field(max_length=100)
  url_gambar: str = Field(max_length=255)
  deskripsi: str = Field(sa_type=Text)
  id_jenis: int = Field(foreign_key="jenis.id")

  created_at: datetime = Field(default_factory=datetime.utcnow)
  updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": func.now()})

  # relationship
  keranjang: List["Keranjang"] = Relationship(back_populates="item")
  jenis: "Jenis" = Relationship(back_populates="items")
  detail_transaksi: List["DetailTransaksi"] = Relationship(back_populates="item")