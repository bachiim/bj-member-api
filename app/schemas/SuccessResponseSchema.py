from pydantic import BaseModel
from typing import Optional, Any, Generic, TypeVar

T = TypeVar("T")

class SuccessResponse(BaseModel, Generic[T]):
  success: bool = True
  message: str = None
  data: Optional[T] = None