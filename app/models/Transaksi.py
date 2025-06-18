from sqlmodel import SQLModel, Field, func
from datetime import datetime
from enum import Enum

class StatusTransaksi(str, Enum):
  PROSES = "proses"
  SELESAI = "selesai"
  BATAL = "batal"


class Transaksi(SQLModel, table=True):
  __tablename__ = "transaksi"

  id: int = Field(primary_key=True, default=None)
  id_member: int = Field(foreign_key="members.id")
  potongan: float = Field()
  total: int = Field()
  status: StatusTransaksi = Field(max_length=30)
  tanggal: datetime = Field()

  created_at: datetime = Field(default_factory=datetime.utcnow)
  updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": func.now()})