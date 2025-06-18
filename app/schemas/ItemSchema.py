from pydantic import BaseModel
from typing import List

from app.schemas.SatuanSchema import SatuanPublic

class HargaSatuan(SatuanPublic):
  harga: float

class ItemPublic(BaseModel):
  id: str
  nama: str
  url_gambar: str
  deskripsi: str
  jenis: str
  satuan: List[HargaSatuan]
  stok: int

class ItemKeranjang(BaseModel):
  id: str
  nama: str
  url_gambar: str
