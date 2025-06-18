from sqlmodel import select

from app.models.Jenis import Jenis
from app.core.database import get_app_session

def seed_jenis():
  session = get_app_session()
  db = next(session)

  if db.exec(select(Jenis)).first():
    print("Data Jenis sudah ada, seeding dibatalkan.")
    return
  
  data = [
    Jenis(nama="MAKANAN"), Jenis(nama="MINUMAN"), Jenis(nama="GALVALUM"), Jenis(nama="PAKAN"),
    Jenis(nama="ATAP"), Jenis(nama="MURBAUT"), Jenis(nama="ALAT"), Jenis(nama="AKSESORIS"),
    Jenis(nama="BESI"), Jenis(nama="BESI BETON"), Jenis(nama="BESI SIKU"), Jenis(nama="PAPAN"),
    Jenis(nama="BESI VIRKAN"), Jenis(nama="CNP"), Jenis(nama="PKG"), Jenis(nama="PKH"),
    Jenis(nama="PKP"), Jenis(nama="PIPA AIR"), Jenis(nama="PLAT GALVANIS"), Jenis(nama="PIPA GAS"),
    Jenis(nama="PLAT HITAM"), Jenis(nama="STRIP"), Jenis(nama="UNP"), Jenis(nama="BIAYA"), Jenis(nama="WF"),
  ]

  db.add_all(data)
  db.commit()
  db.close()

  print("Seeder jenis berhasil dijalankan")