from pydantic import BaseModel

class ErrorSchema(BaseModel):
  success: str = False
  message: str

ErrorResponse = {
  422: {
    "description": "Validation Error",
    "model": ErrorSchema
  },
}