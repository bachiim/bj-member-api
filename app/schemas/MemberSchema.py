from pydantic import BaseModel

class MemberPublic(BaseModel):
  id: int
  nama: str
  telepon: str