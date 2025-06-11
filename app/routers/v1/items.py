from fastapi import APIRouter, HTTPException
from sqlmodel import select
from typing import List

from app.core.database import IposSessionDep
from app.models.Item import Item
from app.schemas.ItemSchema import *
from app.schemas.SuccessResponseSchema import SuccessResponse

router = APIRouter(prefix="/items", tags=["items"])

# read
@router.get("/", response_model=SuccessResponse[List[ItemPublic]])
def read(ipos_session: IposSessionDep):
  try:
    items = ipos_session.exec(select(Item)).all()

    return SuccessResponse(
      message="Berhasil mengambil data item",
      data=[ItemPublic(**item.model_dump()) for item in items]
    )
  
  except HTTPException as e:
    raise HTTPException(status_code=500, detail=str(e))