from sqlmodel import select

from app.models.Satuan import Satuan
from app.core.database import get_app_session

def seed_satuan():
  session = get_app_session()
  db = next(session)

  if db.exec(select(Satuan)).first():
    print("Data Satuan sudah ada, seeding dibatalkan.")
    return
  
  data = [
    Satuan(nama="PCS"), Satuan(nama="DUS"), Satuan(nama="PAK"), Satuan(nama="m"),
    Satuan(nama="kg"), Satuan(nama="ROL"), Satuan(nama="gram"), Satuan(nama="km"),
    Satuan(nama="100pcs"), Satuan(nama="200pcs"), Satuan(nama="850pcs"),
    Satuan(nama="1000pcs"), Satuan(nama="kubik"), Satuan(nama="REET / 10,8kubik")
  ]

  db.add_all(data)
  db.commit()
  db.close()

  print("Seeder satuan berhasil dijalankan")