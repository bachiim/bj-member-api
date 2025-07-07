from sqlmodel import SQLModel, Field
from datetime import datetime, timedelta

class Otp(SQLModel, table=True):
  __tablename__ = "otp"

  id: int|None = Field(primary_key=True, default=None)
  email: str = Field(max_length=100, nullable=False)
  kode_otp: str = Field(max_length=6, nullable=False)

  created_at: datetime = Field(default_factory=datetime.utcnow)
  expired_at: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(minutes=5))
