from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.core.database import IposSessionDep, AppSessionDep
from app.models.Item import Item
from app.models.ItemApp import ItemApp
from app.models.Satuan import Satuan
from app.models.ItemHJ import ItemHJ
from app.schemas.ItemSchema import *
from app.schemas.SuccessResponseSchema import SuccessResponse
from app.utils.hargajual_helper import get_list_hargasatuan_by_id

router = APIRouter(prefix="/items", tags=["items"])

# read
@router.get("/", response_model=SuccessResponse[List[ItemPublic]])
def read(ipos_session: IposSessionDep, app_session: AppSessionDep):
  try:
    items = ipos_session.exec(select(Item)).all()
    items_app = app_session.exec(select(ItemApp)).all()
    satuan = app_session.exec(select(Satuan)).all()
    items_hj = ipos_session.exec(select(ItemHJ).where(ItemHJ.level.in_(["0", "1"]))).all()
    # mapping
    items_map = {item.kodeitem: item for item in items}
    satuan_map = {s.nama: s for s in satuan}

    # grouping ItemHJ by kodeitem
    items_hj_map = {}
    for hj in items_hj:
      items_hj_map.setdefault(hj.kodeitem, []).append(hj)

    data_item = []
    for item_app in items_app:
      item = items_map.get(item_app.id)
      if not item: continue
      itemhj_list = items_hj_map.get(item_app.id, [])
      list_harga = get_list_hargasatuan_by_id(item, satuan_map, itemhj_list)

      data_item.append(ItemPublic(
        id=item_app.id,
        nama=item_app.nama,
        url_gambar=item_app.url_gambar,
        deskripsi=item_app.deskripsi,
        jenis=item_app.jenis.nama,
        satuan=list_harga,
        stok=item.stok
      ))

    return SuccessResponse(
      message="Berhasil mengambil data item",
      data=data_item
    )
  
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))