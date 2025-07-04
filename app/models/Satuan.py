from sqlmodel import SQLModel, Field, func, Relationship
from datetime import datetime
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
  from app.models.Keranjang import Keranjang
  from .DetailTransaksi import DetailTransaksi

class Satuan(SQLModel, table=True):
  __tablename__ = "satuan"

  id: int|None = Field(primary_key=True, default=None)
  nama: str = Field(max_length=50)
  
  created_at: datetime = Field(default_factory=datetime.utcnow)
  updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": func.now()})

  # relationship
  keranjang: List["Keranjang"] = Relationship(back_populates="satuan")
  detail_transaksi: List["DetailTransaksi"] = Relationship(back_populates="satuan")