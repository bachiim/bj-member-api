from pydantic import BaseModel, AfterValidator, EmailStr, model_validator
from pydantic_core import PydanticCustomError
from typing_extensions import Self
from typing import Annotated

from app.utils.validators import *

class RegisterSchema(BaseModel):
  nama: Annotated[str, AfterValidator(max_length("Nama", 100))]
  alamat: str
  telepon: Annotated[str, AfterValidator(max_length("Telepon", 12)), AfterValidator(telepon_format)]
  kota: Annotated[str, AfterValidator(max_length("Kota", 50))]
  email: EmailStr
  password: Annotated[str, AfterValidator(min_length("Password", 8))]
  konfirmasi_password: Annotated[str, AfterValidator(min_length("Konfirmasi Password", 8))]
  ref_member: str|None = None
  ref_sales: str|None = None

  @model_validator(mode="after")
  def check_password_match(self) -> Self:
    if self.password != self.konfirmasi_password:
      raise PydanticCustomError("password_not_match", "Possword dan Konfirmasi Password tidak cocok")
    return self
  
class LoginSchema(BaseModel):
  telepon_email: str
  password: Annotated[str, AfterValidator(min_length("Password", 8))]

class Token(BaseModel):
  access_token: str
  refresh_token: str
  token_type: str

class RefreshTokenSchema(BaseModel):
  refresh_token: str

class ChangePasswordSchema(BaseModel):
  password_lama: Annotated[str, AfterValidator(min_length("Password Lama", 8))]
  password_baru: Annotated[str, AfterValidator(min_length("Password Baru", 8))]
  konfirmasi_password: Annotated[str, AfterValidator(min_length("Konfirmasi", 8))]
  
  @model_validator(mode="after")
  def check_password_match(self) -> Self:
    if self.password_baru != self.konfirmasi_password:
      raise PydanticCustomError("password_not_match", "Possword Baru dan Konfirmasi Password tidak cocok")
    return self
  
class EmailSchema(BaseModel):
  email: EmailStr

class OtpSchema(BaseModel):
  email: EmailStr
  kode_otp: str
