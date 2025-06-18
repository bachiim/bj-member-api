from sqlmodel import select
from typing import List

from app.core.database import AppSessionDep, IposSessionDep

from app.models.Item import Item
from app.models.ItemHJ import ItemHJ
from app.models.Satuan import Satuan

from app.schemas.ItemSchema import HargaSatuan


def get_list_hargasatuan_by_id(id_item: str, app_session: AppSessionDep, ipos_session: IposSessionDep):
  list_harga: List[HargaSatuan] = []
  # get item
  item = ipos_session.exec(select(Item).where(Item.kodeitem == id_item)).first()
  # get satuan
  satuan = app_session.exec(select(Satuan)).all()
  satuan_map = {s.nama: s for s in satuan}

  if item.sistemhargajual == "O":
    item_satuan = satuan_map.get(item.satuan)
    list_harga.append(HargaSatuan(
      id=item_satuan.id,
      nama=item_satuan.nama,
      harga=item.hargajual1
    ))
  else:
    itemhj = ipos_session.exec(
      select(ItemHJ).
      where(ItemHJ.kodeitem == id_item,
            ItemHJ.level.in_(["0", "1"]))
      ).all()
    for hj in itemhj:
      item_satuan = satuan_map.get(hj.satuan)
      list_harga.append(HargaSatuan(
        id=item_satuan.id,
        nama=item_satuan.nama,
        harga=hj.hargajual
      ))

  return list_harga

def get_hargasatuan_by_id(id_item: str, satuan: str, app_session: AppSessionDep, ipos_session: IposSessionDep):
  # get satuan
  item_satuan = app_session.exec(select(Satuan).where(Satuan.nama == satuan)).first()
  # get item
  item = ipos_session.exec(select(Item).where(Item.kodeitem == id_item)).first()
  if item.sistemhargajual == "O":
    harga = item.hargajual1
  else:
    itemhj = ipos_session.exec(
      select(ItemHJ).
      where(ItemHJ.kodeitem == id_item,
            ItemHJ.satuan == satuan,
            ItemHJ.level.in_(["0", "1"]))
    ).first()
    harga =  itemhj.hargajual

  return HargaSatuan(
    id=item_satuan.id,
    nama=item_satuan.nama,
    harga=harga
  )