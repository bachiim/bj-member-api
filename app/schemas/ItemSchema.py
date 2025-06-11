from pydantic import BaseModel

class ItemPublic(BaseModel):
  kodeitem: str
  namaitem: str
  jenis: str
  hargajual1: float
  stok: float
