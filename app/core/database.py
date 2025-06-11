from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, Session

from .config import settings

ipos_engine = create_engine(settings.IPOS_DB_URL, echo=True)
app_engine = create_engine(settings.APP_DB_URL, echo=True)

def get_ipos_session():
  with Session(ipos_engine) as session:
    yield session

def get_app_session():
  with Session(app_engine) as session:
    yield session

IposSessionDep = Annotated[Session, Depends(get_ipos_session)]
AppSessionDep = Annotated[Session, Depends(get_app_session)]