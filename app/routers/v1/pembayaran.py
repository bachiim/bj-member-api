from fastapi import APIRouter, HTTPException, Form
from sqlmodel import select
from typing import Annotated
from datetime import datetime, date
import os

from app.core.database import AppSessionDep, IposSessionDep
from app.core.security import MemberDep
from app.core.supabase import supabase

from app.models.Pembayaran import Pembayaran, StatusPembayaran
from app.models.Transaksi import Transaksi, StatusTransaksi
from app.models.PesanHD import PesanHD
from app.models.PesanDT import PesanDT

from app.schemas.PembayaranSchema import *
from app.schemas.SuccessResponseSchema import SuccessResponse

router = APIRouter(prefix="/pembayaran", tags=["pembayaran"])

FOLDER_PATH = "bukti_transfer"
ALLOWED_EXTENSIONS = ["jpg", "jpeg", "png"]
MAX_FILE_SIZE_MB = 2

@router.post("/", response_model=SuccessResponse[PembayaranPublic])
def create(pembayaran: Annotated[PembayaranCreate, Form()], current_member: MemberDep, app_session: AppSessionDep):
  try:
    transaksi = app_session.exec(select(Transaksi).where(Transaksi.id == pembayaran.id_transaksi)).first()
    if not transaksi:
      raise HTTPException(404, "Transaksi tidak ditemukan")
    
    # validasi ekstensi
    ext = pembayaran.bukti_transfer.filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
      raise HTTPException(422, "Format bukti transfer tidak didukung. Hanya jpg, jpeg, png")
    
    # validasi ukuran file
    contents = pembayaran.bukti_transfer.file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
      raise HTTPException(422, "Ukuran bukti transfer melebihi 2MB")
    
    # rename filename
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    new_filename = f"btf-{timestamp}-{transaksi.id}.{ext}"

    # save file
    # os.makedirs(FOLDER_PATH, exist_ok=True)
    # with open(os.path.join(FOLDER_PATH, new_filename), "wb") as f:
    #   f.write(contents)
    storage_path = f"{FOLDER_PATH}/{new_filename}"
    supabase.storage.from_("uploads").upload(path=storage_path, file=contents)
    
    db_pembayaran = Pembayaran(
      id_transaksi = transaksi.id,
      bukti_transfer=new_filename,
      total=transaksi.total,
      status=StatusPembayaran.MENUNGGU_KONFIRMASI
    )

    app_session.add(db_pembayaran)
    app_session.flush()
    app_session.refresh(db_pembayaran)

    # update status transaksi
    transaksi.status = StatusTransaksi.MENUNGGU_KONFIRMASI
    app_session.commit()

    return SuccessResponse(
      message="Berhasil melakukan pembayaran",
      data=PembayaranPublic(
        id=db_pembayaran.id,
        id_transaksi=db_pembayaran.id_transaksi,
        tanggal=db_pembayaran.created_at,
        total=db_pembayaran.total,
        status=db_pembayaran.status
      )
    )

  except HTTPException:
    app_session.rollback()
    raise
  except Exception as e:
    app_session.rollback()
    raise HTTPException(500, detail=str(e))
  
# konfirmasi pembayaran
@router.post("/konfirmasi/{id}", response_model=SuccessResponse[PembayaranPublic])
def konfirmasi(id: int, request: PembayaranKonfirmasi, current_member: MemberDep, app_session: AppSessionDep, ipos_session: IposSessionDep):
  try:
    pembayaran = app_session.exec(select(Pembayaran).where(Pembayaran.id == id)).first()
    if not pembayaran:
      raise HTTPException(404, detail="Pembayaran tidak ditemukan")
    
    if request.konfirmasi:
      pembayaran.status = StatusPembayaran.BERHASIL

      now = datetime.utcnow()
      start_date = date(now.year, now.month, 1)
      end_date = date(now.year + int(now.month == 12), (now.month % 12) + 1, 1)

      all_transaksi_bulan_ini = app_session.exec(
          select(Transaksi)
          .where(
            Transaksi.tanggal >= start_date,
            Transaksi.tanggal < end_date
          )
          .order_by(Transaksi.tanggal)
      ).all()
      
      urutan_transaksi = 0
      for urutan, transaksi in enumerate(all_transaksi_bulan_ini, 1):
        if transaksi.id == pembayaran.transaksi.id:
          urutan_transaksi = urutan
          break

      transaksi = pembayaran.transaksi
      detail_transaksi = transaksi.details
      total_item = sum([dt.jumlah for dt in detail_transaksi])
      potongan = float(transaksi.potongan * 100)
      
      # create pesanan
      bulan_tahun = datetime.now().strftime("%m%y")
      # bulan_tahun = f"{bulan_tahun[:2]}{bulan_tahun[-2:4]}"
      no_transaksi = f"{urutan_transaksi:04}/ONL/BJ1/{bulan_tahun}"
      pesan_hd = PesanHD(
        notransaksi=no_transaksi,
        kodekantor="BJ1",
        kantortujuan="BJ1",
        tanggal=datetime.now(),
        tipe="OJ",
        tanggalkirim=datetime.now(),
        jenis="JL",
        kodesupel="UMUM",
        matauang="IDR",
        rate=1.0,
        totalitem=total_item,
        subtotal=transaksi.subtotal,
        potfaktur=potongan,
        totalakhir=transaksi.total,
        biaya_msk_total=False,
        user1="ADMIN",
        dateupd=datetime.utcnow(),
        potnomfaktur=transaksi.subtotal * transaksi.potongan,
        dppesanan=pembayaran.total,
        acc_dppesanan="2-3100",
        acc_dpkas="1-1110"
      )

      ipos_session.add(pesan_hd)
      ipos_session.flush()

      # create pesanan detail
      for baris, detail_item in enumerate(detail_transaksi, 1):
        timestamp = int(datetime.utcnow().timestamp() * 1e6)
        id_detail = f"{no_transaksi}-BJ1-{timestamp}-{baris}"
        ipos_session.add(PesanDT(
          iddetail=id_detail,
          nobaris=baris,
          notransaksi=no_transaksi,
          kodeitem=detail_item.id_item,
          jumlah=detail_item.jumlah,
          satuan=detail_item.satuan.nama,
          harga=detail_item.harga,
          total=detail_item.subtotal,
          dateupd=datetime.utcnow()
        ))

        ipos_session.flush()

      # update transaksi
      transaksi.status = StatusTransaksi.PROSES
      transaksi.id_pesanan = no_transaksi

    else:
      pembayaran.status = StatusPembayaran.GAGAL
      pembayaran.keterangan = request.keterangan
      pembayaran.transaksi.status = StatusTransaksi.BATAL

    ipos_session.commit()
    app_session.commit()
    app_session.refresh(pembayaran)

    return SuccessResponse(
      message="Berhasil menngonfirmasi pembayaran",
      data=PembayaranPublic(
        **pembayaran.model_dump(), 
        tanggal=pembayaran.created_at
      )
    )

  except HTTPException:
    app_session.rollback()
    ipos_session.rollback()
    raise
  except Exception as e:
    app_session.rollback()
    ipos_session.rollback()
    raise HTTPException(500, detail=str(e))