from sqlmodel import select

from app.models.Level import Level
from app.core.database import get_app_session

def seed_level():
  session = get_app_session()
  db = next(session)

  if db.exec(select(Level)).first():
    print("Data Level sudah ada, seeding dibatalkan.")
    return
  
  data = [
    Level(nama="bronze", potongan=0.01),
    Level(nama="silver", potongan=0.015),
    Level(nama="gold", potongan=0.02)
  ]

  db.add_all(data)
  db.commit()
  db.close()

  print("Seeder Level berhasil dijalankan")