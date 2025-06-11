from fastapi import APIRouter, HTTPException
from sqlmodel import select
from typing import List

from app.core.database import AppSessionDep
from app.models.Sales import Sales
from app.schemas.SalesSchema import *
from app.schemas.SuccessResponseSchema import SuccessResponse
from app.schemas.ErrorResponseSchema import ErrorResponse

router = APIRouter(prefix="/sales", tags=["sales"])

# create
@router.post("/", response_model=SuccessResponse[SalesPublic], responses=ErrorResponse)
def create(sales: SalesCreate, session: AppSessionDep):
  try:
    # telepon unique validation
    exist_sales = session.exec(select(Sales).where(Sales.telepon == sales.telepon)).first()
    if exist_sales:
      raise HTTPException(status_code=422, detail="Telepon sudah terdaftar")
    
    # save to db
    db_sales = Sales.model_validate(sales)
    session.add(db_sales)
    session.commit()
    session.refresh(db_sales)

    return SuccessResponse[SalesPublic](
      message="Berhasil mendaftarkan data sales",
      data=SalesPublic(**db_sales.model_dump())
    )
  
  except HTTPException as e:
    session.rollback()
    raise e

# read
@router.get("/", response_model=SuccessResponse[List[SalesPublic]])
def read(session: AppSessionDep):
  try:
    sales = session.exec(select(Sales)).all()

    return SuccessResponse(
      message="Berhasil mengambil data sales",
      data=[SalesPublic(**sale.model_dump()) for sale in sales]
    )
  except HTTPException as e:
    HTTPException(status_code=500, detail=str(e))

# show
@router.get("/{id}", response_model=SuccessResponse[SalesPublic], responses=ErrorResponse)
def show(id: int, session: AppSessionDep):
  try:
    sales = session.exec(select(Sales).where(Sales.id == id)).first()
    if not sales:
      raise HTTPException(status_code=404, detail=f"Sales dengan id {id} tidak ditemukan")
    
    return SuccessResponse(
      message=f"Berhasil mengambil data sales dengan id {id}",
      data=SalesPublic(**sales.model_dump())
    )
  
  except HTTPException as e:
    raise e
  
# update
@router.put("/{id}", response_model=SuccessResponse[SalesPublic], responses=ErrorResponse)
def update(id: int, sales: SalesUpdate, session: AppSessionDep):
  try:
    db_sales = session.exec(select(Sales).where(Sales.id == id)).first()
    if not db_sales:
      raise HTTPException(status_code=404, detail=f"Sales dengan id {id} tidak ditemukan")
    
    # telepon unique validation
    exist_sales = session.exec(select(Sales).where(Sales.telepon == sales.telepon, Sales.id != id)).first()
    if exist_sales:
      raise HTTPException(status_code=422, detail="Telepon sudah terdaftar")
    
    # update db
    data_sales = sales.model_dump(exclude_unset=True)
    db_sales.sqlmodel_update(data_sales)
    session.add(db_sales)
    session.commit()
    session.refresh(db_sales)
    
    return SuccessResponse(
      message=f"Berhasil mengupdate data sales dengan id {id}",
      data=SalesPublic(**db_sales.model_dump())
    )
  
  except HTTPException as e:
    session.rollback()
    raise e
  
# delete
@router.delete("/{id}", response_model=SuccessResponse, responses=ErrorResponse)
def delete(id: int, session: AppSessionDep):
  try:
    db_sales = session.exec(select(Sales).where(Sales.id == id)).first()
    if not db_sales:
      raise HTTPException(status_code=404, detail=f"Sales dengan id {id} tidak ditemukan")
    
    session.delete(db_sales)
    session.commit()

    return SuccessResponse(message=f"Berhasil menghapus data sales dengan id {id}")
  
  except HTTPException as e:
    session.rollback()
    raise e
