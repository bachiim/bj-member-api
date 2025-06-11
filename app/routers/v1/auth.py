from fastapi import APIRouter, HTTPException
from sqlmodel import select, or_
from jwt.exceptions import PyJWTError

from app.core.database import AppSessionDep
from app.core.security import get_password_hash, verify_password, authenticate_member, create_token, decode_token, MemberDep

from app.models.Member import Member
from app.models.Sales import Sales

from app.schemas.AuthSchema import *
from app.schemas.SuccessResponseSchema import SuccessResponse
from app.schemas.MemberSchema import MemberPublic
from app.schemas.ErrorResponseSchema import ErrorResponse

router = APIRouter(prefix="/auth", tags=["authentication"])

# register
@router.post("/register", response_model=SuccessResponse[MemberPublic], responses=ErrorResponse)
def register(member: RegisterSchema, session: AppSessionDep):
  try:
    # telepon and email unique validation
    exist_member = session.exec(select(Member).where(or_(Member.telepon == member.telepon, Member.email == member.email))).first()
    if exist_member:
      raise HTTPException(status_code=422, detail="Telepon atau Email sudah terdaftar")
    # referal member
    if member.ref_member:
      referal_member = session.exec(select(Member).where(Member.telepon == member.ref_member)).first()
      if not referal_member:
        raise HTTPException(status_code=422, detail="Referal member tidak valid")
    # referal sales
    if member.ref_sales:
      referal_sales = session.exec(select(Sales).where(Sales.telepon == member.ref_sales)).first()
      if not referal_sales:
        raise HTTPException(status_code=422, detail="Referal sales tidak valid")
    
    db_member = Member(
      nama=member.nama,
      alamat=member.alamat,
      telepon=member.telepon,
      kota=member.kota,
      email=member.email,
      password=get_password_hash(member.password),
      ref_member=referal_member.id if member.ref_member else None,
      ref_sales=referal_sales.id if member.ref_sales else None
    )

    session.add(db_member)
    session.commit()
    session.refresh(db_member)

    return SuccessResponse(
      message="Berhasil mendaftar member",
      data=MemberPublic(**db_member.model_dump())
    )
  
  except HTTPException as e:
    session.rollback()
    raise e
  
  except Exception as e:
    session.rollback()
    raise HTTPException(status_code=500, detail=str(e))
  
# login
@router.post("/login", response_model=SuccessResponse[Token], responses=ErrorResponse)
def login(data: LoginSchema, session: AppSessionDep):
  try:
    member = authenticate_member(data.telepon_email, data.password, session)
    if not member:
      raise HTTPException(status_code=401, detail="Telepon/Email atau Password salah", headers={"WWW-Authenticate": "Bearer"})
    
    access_token = create_token(str(member.id), member.nama, "access")
    refresh_token = create_token(str(member.id), member.nama, "refresh")

    return SuccessResponse(
      message="Berhasil login",
      data=Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
    )

  except HTTPException as e:
    raise e
  
  except Exception as e:
    raise HTTPException(500, detail=str(e))
  
# refresh token
@router.post("/refresh-token", response_model=SuccessResponse[Token], responses=ErrorResponse)
def refresh_token(data: RefreshTokenSchema):
  try:
    payload = decode_token(data.refresh_token)
    id_member = payload.get("sub")
    nama = payload.get("nama")

    if not id_member:
      raise HTTPException(401, detail="Refresh token tidak valid")

    new_access_token = create_token(id_member, nama, "access")

    return SuccessResponse(
      message="Berhasil mendapatkan ulang token",
      data=Token(access_token=new_access_token, refresh_token=data.refresh_token, token_type="bearer")
    )
  
  except HTTPException as e:
    raise e

  except PyJWTError as e:
    raise HTTPException(401, detail=str(e))
  
  except Exception as e:
    raise HTTPException(401, detail=str(e))
  
# change password
@router.post("/change-password", response_model=SuccessResponse, responses=ErrorResponse)
def change_password(data: ChangePasswordSchema, current_member: MemberDep, session: AppSessionDep):
  try:
    member = session.exec(select(Member).where(Member.id == current_member["id"])).first()
    if not member:
      raise HTTPException(401, detail="Autentikasi gagal")
    if not verify_password(data.password_lama, member.password):
      raise HTTPException(402, detail="Password lama salah")
    
    member.password = get_password_hash(data.password_baru)
    session.add(member)
    session.commit()

    return SuccessResponse(message="Berhasil memperbarui password")

  except HTTPException as e:
    session.rollback()
    raise e
  
  except Exception as e:
    session.rollback()
    raise HTTPException(500, detail=str(e))
