from pydantic import BaseModel, AfterValidator
from typing import Annotated

from app.utils.validators import *

class SalesPublic(BaseModel):
  id: int
  nama: str
  telepon: str
  alamat: str

class SalesCreate(BaseModel):
  nama: Annotated[str, AfterValidator(max_length("Nama", 100))]
  alamat: str
  telepon: Annotated[str, AfterValidator(max_length("Telepon", 12)), AfterValidator(telepon_format)]

class SalesUpdate(BaseModel):
  nama: Annotated[str, AfterValidator(max_length("Nama", 100))] | None = None
  alamat: str|None = None
  telepon: Annotated[str, AfterValidator(max_length("Telepon", 12)), AfterValidator(telepon_format)] | None = None