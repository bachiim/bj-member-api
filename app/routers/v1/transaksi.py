from fastapi import APIRouter, HTTPException
from sqlmodel import select
from datetime import datetime
from typing import List

from app.core.security import MemberDep
from app.core.database import AppSessionDep, IposSessionDep

from app.utils.hargajual_helper import get_hargasatuan_by_id

from app.models.Keranjang import Keranjang
from app.models.Member import Member
from app.models.Transaksi import Transaksi, StatusTransaksi
from app.models.DetailTransaksi import DetailTransaksi

from app.schemas.SuccessResponseSchema import SuccessResponse
from app.schemas.TransaksiSchema import *
from app.schemas.DetailTransaksiSchema import *
from app.schemas.ItemSchema import ItemKeranjang, HargaSatuan

router = APIRouter(prefix="/transaksi", tags=["transaksi"])

# create transaksi
@router.post("/", response_model=SuccessResponse[TransaksiPublic])
def create(current_member: MemberDep, app_session: AppSessionDep, ipos_session: IposSessionDep):
  try:
    member = app_session.exec(select(Member).where(Member.id == current_member.get("id"))).first()
    items_keranjang = app_session.exec(select(Keranjang).where(Keranjang.id_member == member.id)).all()
    if not items_keranjang:
      raise HTTPException(status_code=400, detail="Keranjang kosong")
    
    items = []
    for item in items_keranjang:
      harga_satuan = get_hargasatuan_by_id(item.id_item, item.satuan.nama, app_session, ipos_session)
      items.append({
        "id_item": item.id_item,
        "jumlah": item.jumlah,
        "id_satuan": item.id_satuan,
        "satuan": item.satuan.nama,
        "harga": harga_satuan.harga,
        "subtotal": item.jumlah * harga_satuan.harga
      })

    subtotal = sum(item["subtotal"] for item in items)
    potongan = member.level.potongan
    nominal_potongan = subtotal * potongan
    total = subtotal - nominal_potongan

    # create transaksi
    transaksi = Transaksi(
      id_member=member.id,
      potongan=potongan,
      subtotal=subtotal,
      total=total,
      status=StatusTransaksi.MENUNGGU_PEMBAYARAN,
      tanggal=datetime.utcnow()
    )

    app_session.add(transaksi)
    app_session.flush()
    app_session.refresh(transaksi)

    # create detail transaksi
    for item in items:
      app_session.add(DetailTransaksi(
        id_transaksi=transaksi.id,
        id_item=item["id_item"],
        id_satuan=item["id_satuan"],
        jumlah=item["jumlah"],
        harga=item["harga"],
        subtotal=item["subtotal"]
      ))

    # delete keranjang
    for item in items_keranjang:
      app_session.delete(item)

    app_session.commit()
    app_session.refresh(transaksi)

    return SuccessResponse(
      message="Transaksi berhasil dibuat",
      data=TransaksiPublic(**transaksi.model_dump())
    )

  except HTTPException:
    app_session.rollback()
    raise
  except Exception as e:
    app_session.rollback()
    raise HTTPException(status_code=500, detail=str(e))
  
# get
@router.get("/", response_model=SuccessResponse[List[TransaksiWithDetails]])
def get(current_member: MemberDep, app_session: AppSessionDep):
  try:
    transaksi = app_session.exec(select(Transaksi)
                                 .where(Transaksi.id_member == current_member.get("id"))
                                 .order_by(Transaksi.tanggal.desc())).all()

    data = []
    if transaksi:
      for t in transaksi:
        data.append(TransaksiWithDetails(
          **t.model_dump(),
          details=[DetailTransaksiPublic(
            **d.model_dump(),
            item=ItemKeranjang(**d.item.model_dump()),
            satuan=HargaSatuan(**d.satuan.model_dump(), harga=d.harga)
          )
            for d in t.details
          ]
        ))

    return SuccessResponse(message="Transaksi berhasil diambil", data=data)

  except HTTPException:
    raise
  except Exception as e:
    raise HTTPException(500, detail=str(e))