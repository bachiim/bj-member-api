import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel import select, or_
from datetime import timedelta, datetime
from typing import Annotated

from .database import AppSessionDep
from .config import settings

from app.models.Member import Member
from app.schemas.MemberSchema import MemberPublic

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_password_hash(password: str):
  return bcrypt_context.hash(password)

def verify_password(plain_password, hashed_password):
  return bcrypt_context.verify(plain_password, hashed_password)

def decode_token(token: str):
  return jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)

def authenticate_member(telepon_email: str, password: str, session: AppSessionDep):
  member = session.exec(select(Member).where(or_(Member.telepon == telepon_email, Member.email == telepon_email))).first()
  if not member:
    return False
  if not verify_password(password, member.password):
    return False
  return member

def create_token(id_member: str, nama: str, token_type: str):
  to_encode = {"sub": id_member, "nama": nama}
  if token_type == "access":
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
  if token_type == "refresh":
    expire = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS) 
  to_encode.update({"exp": expire})

  return jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)

async def get_current_member(token: Annotated[str, Depends(oauth2_bearer)]):
  try:
    payload = decode_token(token)
    id_member = payload.get("sub")
    nama = payload.get("nama")
    if id_member is None:
      raise HTTPException(401, detail="Tidak dapat memvalidasi kredensial", headers={"WWW-Authenticate": "Bearer"})
    
    return {"id": id_member, "nama": nama}

  except InvalidTokenError as e:
    raise HTTPException(401, detail=str(e), headers={"WWW-Authenticate": "Bearer"})
  

MemberDep = Annotated[dict, Depends(get_current_member)]
