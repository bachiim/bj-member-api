from sqlmodel import SQLModel, Field, func
from datetime import datetime

class DetailSatuanItem(SQLModel, table=True):
  __tablename__ = "detail_satuan_item"

  id: int|None = Field(primary_key=True, default=None)
  id_item: str = Field(foreign_key="items.id")
  id_satuan: int = Field(foreign_key="satuan.id")

  created_at: datetime = Field(default_factory=datetime.utcnow)
  updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": func.now()})