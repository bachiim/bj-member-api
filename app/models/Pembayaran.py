from sqlmodel import SQLModel, Field, func, Relationship, Text
from datetime import datetime
from typing import TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
  from .Transaksi import Transaksi

class StatusPembayaran(str, Enum):
  MENUNGGU_KONFIRMASI = "menunggu konfirmasi"
  BERHASIL = "berhasil"
  GAGAL = "gagal"

class Pembayaran(SQLModel, table=True):
  __tablename__ = "pembayaran"

  id: int|None = Field(primary_key=True, default=None)
  id_transaksi: int = Field(foreign_key="transaksi.id", nullable=False)
  bukti_transfer: str = Field(nullable=False)
  total: int = Field(nullable=False)
  status: StatusPembayaran = Field(max_length=30, nullable=False)
  keterangan: str|None = Field(default=None, sa_type=Text)
  
  created_at: datetime = Field(default_factory=datetime.utcnow)
  updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": func.now()})
  
  # relationhip
  transaksi: "Transaksi" = Relationship(back_populates="pembayaran")
