from pydantic import BaseModel
from fastapi import UploadFile
from datetime import datetime

from app.models.Pembayaran import StatusPembayaran

class PembayaranPublic(BaseModel):
  id: int
  id_transaksi: int
  tanggal: datetime
  total: int
  status: StatusPembayaran
  keterangan: str|None = None

class PembayaranCreate(BaseModel):
  id_transaksi: int
  bukti_transfer: UploadFile

class PembayaranKonfirmasi(BaseModel):
  konfirmasi: bool
  keterangan: str|None = None