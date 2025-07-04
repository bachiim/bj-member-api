from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException

from .exceptions import validation_exception_handler, http_exception_handler
from .routers.v1 import items, sales, auth, members, keranjang, transaksi, pembayaran

from app.schemas.ErrorResponseSchema import ErrorResponse

app = FastAPI(title="BJ Member API", responses=ErrorResponse)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(members.router, prefix="/api/v1")
app.include_router(items.router, prefix="/api/v1")
app.include_router(keranjang.router, prefix="/api/v1")
app.include_router(transaksi.router, prefix="/api/v1")
app.include_router(pembayaran.router, prefix="/api/v1")
# app.include_router(sales.router, prefix="/api/v1")

@app.get('/')
def root():
  return "API is working now 😎"