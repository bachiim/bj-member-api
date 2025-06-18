from sqlmodel import SQLModel, Field, Numeric
from datetime import datetime

class ItemHJ(SQLModel, table=True):
  __tablename__ = "tbl_itemhj"

  iddetail: str = Field(primary_key=True, max_length=150)
  kodeitem: str|None = Field(max_length=100)
  tipehj: str|None = Field(max_length=10)
  jmlsampai: float|None = Field(default=0, sa_type=Numeric(20, 3))
  level: int|None = Field(default=0)
  prosentase: float|None = Field(default=0, sa_type=Numeric(20, 3))
  satuan: str|None = Field(max_length=50)
  hargajual: float|None = Field(default=0, sa_type=Numeric(20, 3))
  dateupd: datetime|None = Field()