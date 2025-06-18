from pydantic import BaseModel

from app.schemas.ItemSchema import ItemKeranjang, HargaSatuan

class KeranjangPublic(BaseModel):
  id: int
  item: ItemKeranjang
  satuan: HargaSatuan
  jumlah: int

class KeranjangCreate(BaseModel):
  id_item: str
  id_satuan: int
  jumlah: int

class KeranjangUpdate(BaseModel):
  id_satuan: int|None = None
  jumlah: int|None = None