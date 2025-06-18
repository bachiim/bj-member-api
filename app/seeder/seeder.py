from app.seeder.jenis_seeder  import seed_jenis
from app.seeder.satuan_seeder  import seed_satuan
from app.seeder.level_seeder import seed_level
from app.seeder.sales_seeder import seed_sales
from app.seeder.members_seeder import seed_member

if __name__ == "__main__":
  seed_jenis()
  seed_satuan()
  seed_level()
  seed_sales()
  seed_member()