from pydantic import BaseModel

from .ItemSchema import ItemKeranjang, HargaSatuan

class DetailTransaksiPublic(BaseModel):
  item: ItemKeranjang
  satuan: HargaSatuan
  jumlah: int
  subtotal: int