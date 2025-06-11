from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.core.database import AppSessionDep
from app.core.security import MemberDep

from app.models.Member import Member

from app.schemas.SuccessResponseSchema import SuccessResponse
from app.schemas.MemberSchema import MemberPublic

router = APIRouter(prefix="/members", tags=["members"])

@router.get("/me", response_model=SuccessResponse[MemberPublic])
def me(current_member: MemberDep, session: AppSessionDep):
  try:
    db_member = session.exec(select(Member).where(Member.id == int(current_member["id"]))).first()
    if db_member is None:
      raise HTTPException(401, detail="Autentikasi gagal")
    
    return SuccessResponse(
      message="Berhasil mendapatkan data member",
      data=MemberPublic(**db_member.model_dump())
    )
  
  except HTTPException as e:
    raise e
  