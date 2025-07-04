from fastapi import APIRouter, HTTPException
from typing import Dict, List
from sqlmodel import select, func
from collections import defaultdict

from app.core.database import AppSessionDep, IposSessionDep
from app.core.security import MemberDep

from app.models.Keranjang import Keranjang
from app.models.Item import Item
from app.models.ItemHJ import ItemHJ
from app.models.ItemApp import ItemApp
from app.models.Satuan import Satuan

from app.schemas.KeranjangSchema import *
from app.schemas.ItemSchema import ItemKeranjang
from app.schemas.SuccessResponseSchema import SuccessResponse
from app.schemas.ErrorResponseSchema import ErrorResponse

from app.utils.hargajual_helper import get_hargasatuan_by_id


router = APIRouter(prefix="/keranjang", tags=["keranjang"])

# add
@router.post("/", response_model=SuccessResponse[KeranjangPublic], responses=ErrorResponse)
def add(keranjang: KeranjangCreate, current_member: MemberDep, app_session: AppSessionDep, ipos_session: IposSessionDep):
  try:
    # cek item
    item = app_session.exec(select(ItemApp).where(ItemApp.id == keranjang.id_item)).first()
    if not item:
      raise HTTPException(status_code=404, detail="Item tidak ditemukan")
    # cek satuan
    satuan = app_session.exec(select(Satuan).where(Satuan.id == keranjang.id_satuan)).first()
    if not satuan:
      raise HTTPException(status_code=404, detail="Satuan tidak ditemukan")
    # cek keranjang
    keranjang_exist = app_session.exec(
      select(Keranjang).
      where(Keranjang.id_member == current_member.get("id"),
            Keranjang.id_item == keranjang.id_item,
            Keranjang.id_satuan == keranjang.id_satuan)
      ).first()
    if keranjang_exist:
      # get harga jual
      harga_satuan = get_hargasatuan_by_id(keranjang_exist.id_item, keranjang_exist.satuan.nama, app_session, ipos_session)
      # tambah jumlah
      keranjang_exist.jumlah += keranjang.jumlah
      app_session.commit()
      app_session.refresh(keranjang_exist)

      return SuccessResponse(
        message="Berhasil menambahkan item ke keranjang",
        data=KeranjangPublic(
          id=keranjang_exist.id,
          item=ItemKeranjang(**keranjang_exist.item.model_dump()),
          satuan=harga_satuan,
          jumlah=keranjang_exist.jumlah
        )
      )
    
    harga_satuan = get_hargasatuan_by_id(keranjang.id_item, satuan.nama, app_session, ipos_session)
    
    db_keranjang = Keranjang(
      id_member=current_member.get("id"),
      id_item=keranjang.id_item,
      id_satuan=keranjang.id_satuan,
      jumlah=keranjang.jumlah
    )

    app_session.add(db_keranjang)
    app_session.commit()
    app_session.refresh(db_keranjang)

    return SuccessResponse[KeranjangPublic](
      message="Berhasil menambahkan item ke keranjang",
      data=KeranjangPublic(
        id=db_keranjang.id,
        item=ItemKeranjang(**db_keranjang.item.model_dump()),
        satuan=harga_satuan,
        jumlah=db_keranjang.jumlah
      )
    )
    
  except HTTPException:
    app_session.rollback()
    raise

  except Exception as e:
    app_session.rollback()
    raise HTTPException(500, detail=str(e))


# get
@router.get("/", response_model=SuccessResponse[List[KeranjangPublic]])
def get(current_member: MemberDep, app_session: AppSessionDep, ipos_session: IposSessionDep):
  try:
    # get item keranjang
    keranjang = app_session.exec(select(Keranjang).where(Keranjang.id_member == current_member.get("id"))).all()
  
    if keranjang:
      # get items
      item_ipos = ipos_session.exec(select(Item)).all()
      item_ipos_map = {item.kodeitem: item for item in item_ipos} # map item by kodeitem
      # get itemhj
      item_hj = ipos_session.exec(select(ItemHJ).where(ItemHJ.level.in_(["0", "1"]))).all()
      item_hj_map: Dict[str, List[ItemHJ]] = defaultdict(list)
      # map itemhj by kodeitem
      for item in item_hj:
        item_hj_map[item.kodeitem].append(item)

      data_item = []
      for k in keranjang:
        harga_satuan = get_hargasatuan_by_id(k.id_item, k.satuan.nama, app_session, ipos_session)

        data_item.append(KeranjangPublic(
          id=k.id,
          item=ItemKeranjang(**k.item.model_dump()),
          satuan=harga_satuan,
          jumlah=k.jumlah
        ))
      
      return SuccessResponse(
        message="Berhasil mengambil data keranjang",
        data=data_item
      )

    return SuccessResponse(
      message="Berhasil mengambil data keranjang",
      data=[]
    )
  except Exception as e:
    raise HTTPException(500, detail=str(e))


# update
@router.put("/{id}", response_model=SuccessResponse[KeranjangPublic], responses=ErrorResponse)
def update(id: int, keranjang: KeranjangUpdate, current_member: MemberDep, app_session: AppSessionDep, ipos_session: IposSessionDep):
  try:
    db_keranjang = app_session.exec(select(Keranjang).where(Keranjang.id == id)).first()
    if not db_keranjang:
      raise HTTPException(status_code=404, detail="Item keranjang tidak ditemukan")
    
    data_keranjang = keranjang.model_dump(exclude_unset=True)
    db_keranjang.sqlmodel_update(data_keranjang)
    app_session.add(db_keranjang)
    app_session.commit()
    app_session.refresh(db_keranjang)

    harga_satuan = get_hargasatuan_by_id(db_keranjang.id_item, db_keranjang.satuan.nama, app_session, ipos_session)
    return SuccessResponse(
      message="Berhasil mengupdate data keranjang",
      data=KeranjangPublic(
        id=db_keranjang.id,
        item=ItemKeranjang(**db_keranjang.item.model_dump()),
        satuan=harga_satuan,
        jumlah=db_keranjang.jumlah
      )
    )

  except HTTPException:
    app_session.rollback()
    raise  

  except Exception as e:
    app_session.rollback()
    raise HTTPException(500, detail=str(e))
  
# delete
@router.delete("/{id}", response_model=SuccessResponse, responses=ErrorResponse)
def delete(id: int, current_member: MemberDep, app_session: AppSessionDep):
  try:
    db_keranjang = app_session.exec(select(Keranjang).where(Keranjang.id == id)).first()
    if not db_keranjang:
      raise HTTPException(404, "Keranjang tidak ditemukan")
    
    app_session.delete(db_keranjang)
    app_session.commit()

  except HTTPException:
    app_session.rollback()
    raise
  except Exception as e:
    app_session.rollback()
    raise HTTPException(500, detail=str(e))