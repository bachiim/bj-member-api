from sqlmodel import SQLModel, Field, Text, func, Relationship
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
  from app.models.Sales import Sales

class Member(SQLModel, table=True):
  __tablename__ = "members"

  id: int|None = Field(primary_key=True, default=None)
  nama: str = Field(max_length=100)
  alamat: str = Field(sa_type=Text)
  telepon: str = Field(max_length=12, unique=True)
  kota: str = Field(max_length=50)
  email: str = Field(max_length=100, unique=True)
  password: str = Field()
  ref_member: int|None = Field(foreign_key="members.id")
  ref_sales: int|None = Field(foreign_key="sales.id")

  created_at: datetime = Field(default_factory=datetime.utcnow)
  updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": func.now()})
  # member relationship
  from_member: Optional["Member"] = Relationship(back_populates="to_member", sa_relationship_kwargs={"remote_side": "Member.id"})
  to_member: List["Member"] = Relationship(back_populates="from_member")
  # sales relationship
  sales: Optional["Sales"] = Relationship(back_populates="members")
  