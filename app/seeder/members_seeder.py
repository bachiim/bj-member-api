from sqlmodel import select

from app.models.Member import Member
from app.core.database import get_app_session
from app.core.security import get_password_hash

def seed_member():
  session = get_app_session()
  db = next(session)

  if db.exec(select(Member)).first():
    print("Data Member sudah ada, seeding dibatalkan.")
    return
  
  data = [
    Member(
      nama="Member Satu", alamat="Jl. satu No.1", telepon="081234567891", kota="Surabaya",
      email="satu@example.com", password=get_password_hash("member01"), ref_member=None, ref_sales=None, id_level=1
    ),
    Member(
      nama="Member Dua", alamat="Jl. dua No.2", telepon="081234567892", kota="Malang",
      email="dua@example.com", password=get_password_hash("member02"), ref_member=None, ref_sales=1, id_level=2
    ),
    Member(
      nama="Member Tiga", alamat="Jl. tiga No.3", telepon="081234567893", kota="Batu",
      email="tiga@example.com", password=get_password_hash("member03"), ref_member=2, ref_sales=3, id_level=3
    ),
  ]

  db.add_all(data)
  db.commit()
  db.close()

  print("Seeder Member berhasil dijalankan")