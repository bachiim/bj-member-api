from fastapi import Request
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

async def validation_exception_handler(request: Request, exc: RequestValidationError):
  errors = [err["msg"] for err in exc.errors()]
  return JSONResponse(
    status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    content={
      "success": False,
      "message": errors[0],
      "errors": errors
    }
  )

async def http_exception_handler(request: Request, exc: HTTPException):
  return JSONResponse(
    status_code=exc.status_code,
    content={
      "success": False,
      "message": exc.detail
    }
  )
