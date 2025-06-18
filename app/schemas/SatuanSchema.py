from pydantic import BaseModel

class SatuanPublic(BaseModel):
  id: int
  nama: str