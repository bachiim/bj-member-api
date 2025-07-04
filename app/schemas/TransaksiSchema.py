from pydantic import BaseModel
from datetime import datetime
from typing import List

from app.models.Transaksi import StatusTransaksi
from .DetailTransaksiSchema import DetailTransaksiPublic

class TransaksiPublic(BaseModel):
  id: int
  tanggal: datetime
  total: int
  status: StatusTransaksi

class TransaksiWithDetails(TransaksiPublic):
  details: List[DetailTransaksiPublic]
  