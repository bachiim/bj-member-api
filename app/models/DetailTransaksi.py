from sqlmodel import SQLModel, Field, func
from datetime import datetime

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