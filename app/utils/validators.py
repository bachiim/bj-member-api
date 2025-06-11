import re
from pydantic_core import PydanticCustomError

def max_length(field_name: str, max_length: int) -> str:
  def validator(value: str) -> str:
    if len(value) > max_length:
      raise PydanticCustomError("string_max_length", f"{field_name} harus memiliki maksimal {max_length} karakter")
    return value
  return validator

def min_length(field_name: str, min_length: int) -> str:
  def validator(value: str) -> str:
    if len(value) < min_length:
      raise PydanticCustomError("string_min_length", f"{field_name} harus memiliki minimal {min_length} karakter")
    return value
  return validator

def telepon_format(value: str) -> str:
  if not re.match(f"^0\d+$", value):
    raise PydanticCustomError("telepon_format", "Telepon harus diawali 0 dan hanya berisi angka")
  return value