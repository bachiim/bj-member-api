from sqlmodel import SQLModel, Field, Numeric, Text
from datetime import datetime

class PesanDT(SQLModel, table=True):
  __tablename__ = "tbl_pesandt"

  iddetail: str = Field(primary_key=True, max_length=150)
  nobaris: int|None = Field(default=0)
  notransaksi: str|None = Field(max_length=50)
  kodeitem: str|None = Field(max_length=100)
  jumlah: float|None = Field(default=0, sa_type=Numeric(20,3))
  jmlterima: float|None = Field(default=0, sa_type=Numeric(20,3))
  satuan: str|None = Field(max_length=50)
  harga: float|None = Field(default=0, sa_type=Numeric(20,3))
  potongan: float|None = Field(default=0, sa_type=Numeric(20,3))
  total: float|None = Field(default=0, sa_type=Numeric(20,3))
  pajak: float|None = Field(default=0, sa_type=Numeric(20,3))
  dateupd: datetime|None = Field()
  detinfo: str|None = Field(sa_type=Text)