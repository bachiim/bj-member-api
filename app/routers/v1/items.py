from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.core.database import IposSessionDep, AppSessionDep
from app.models.Item import Item
from app.models.ItemApp import ItemApp
from app.schemas.ItemSchema import *
from app.schemas.SuccessResponseSchema import SuccessResponse
from app.utils.hargajual_helper import get_list_hargasatuan_by_id

router = APIRouter(prefix="/items", tags=["items"])

# read
@router.get("/", response_model=SuccessResponse[List[ItemPublic]])
def read(ipos_session: IposSessionDep, app_session: AppSessionDep):
  try:
    # get items
    items = ipos_session.exec(select(Item)).all()
    # get items app
    items_app = app_session.exec(select(ItemApp)).all()
    items_app_map = {item.id: item for item in items_app}

    data_item = []
    for item in items:
      list_harga = get_list_hargasatuan_by_id(item.kodeitem, app_session, ipos_session)
      item_app = items_app_map.get(item.kodeitem)

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