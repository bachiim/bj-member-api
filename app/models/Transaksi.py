from sqlmodel import SQLModel, Field, func, Relationship
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
  from .DetailTransaksi import DetailTransaksi
  from .Pembayaran import Pembayaran

class StatusTransaksi(str, Enum):
  MENUNGGU_PEMBAYARAN = "menunggu pembayaran"
  MENUNGGU_KONFIRMASI = "menunggu konfirmasi"
  PROSES = "proses"
  SELESAI = "selesai"
  BATAL = "batal"


class Transaksi(SQLModel, table=True):
  __tablename__ = "transaksi"

  id: int = Field(primary_key=True, default=None)
  id_member: int = Field(foreign_key="members.id")
  id_pesanan: str|None = Field(default=None, unique=True)
  potongan: float = Field()
  subtotal: int = Field()
  total: int = Field()
  status: StatusTransaksi = Field(max_length=30)
  tanggal: datetime = Field()

  created_at: datetime = Field(default_factory=datetime.utcnow)
  updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": func.now()})

  # relationship
  details: List["DetailTransaksi"] = Relationship(back_populates="transaksi")
  pembayaran: "Pembayaran" = Relationship(back_populates="transaksi")