from sqlmodel import SQLModel, Field, func
from datetime import datetime 

class Level(SQLModel, table=True):
  __tablename__ = "levels"

  id: int|None = Field(primary_key=True, default=None)
  nama: str = Field(max_length=50)
  potongan: float = Field()

  created_at: datetime = Field(default_factory=datetime.utcnow)
  updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": func.now()})