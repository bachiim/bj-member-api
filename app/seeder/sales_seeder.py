from sqlmodel import select

from app.models.Sales import Sales
from app.core.database import get_app_session

def seed_sales():
  session = get_app_session()
  db = next(session)

  if db.exec(select(Sales)).first():
    print("Data Sales sudah ada, seeding dibatalkan.")
    return
  
  data = [
    Sales(nama="Sales Satu", alamat="Jl. Raya 1", telepon="081111111111"),
    Sales(nama="Sales Dua", alamat="Jl. Raya 2", telepon="082222222222"),
    Sales(nama="Sales Tiga", alamat="Jl. Raya 3", telepon="083333333333")
  ]

  db.add_all(data)
  db.commit()
  db.close()

  print("Seeder Sales berhasil dijalankan")