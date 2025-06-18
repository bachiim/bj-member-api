import pandas as pd
from app.core.database import ipos_engine, app_engine

# get items from ipos
df_items_ipos = pd.read_sql("SELECT kodeitem, namaitem, jenis FROM tbl_item", ipos_engine)\
# get jenis from app
df_jenis_app = pd.read_sql("SELECT id, nama FROM jenis", app_engine)

df_joined = df_items_ipos.merge(df_jenis_app, left_on="jenis", right_on="nama", how="inner")

df_items_app = pd.DataFrame({
  "id": df_joined["kodeitem"],
  "nama": df_joined["namaitem"],
  "url_gambar": "",
  "deskripsi": "",
  "id_jenis": df_joined["id"]
})

df_items_app.to_csv("items_app_result.csv", index=False)
