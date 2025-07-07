from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  # IPOS DATABASE
  IPOS_DB_USERNAME: str
  IPOS_DB_PASSWORD: str
  IPOS_DB_HOST: str
  IPOS_DB_PORT: str
  IPOS_DB_NAME: str
  # APP DATABASE
  APP_DB_USERNAME: str
  APP_DB_PASSWORD: str
  APP_DB_HOST: str
  APP_DB_PORT: str
  APP_DB_NAME: str
  # JWT
  JWT_SECRET_KEY: str
  JWT_ALGORITHM: str
  JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int
  JWT_REFRESH_TOKEN_EXPIRE_DAYS: int
  # SUPABASE
  SUPABASE_URL: str
  SUPABASE_KEY: str
  # MAIL
  MAIL_USERNAME: str
  MAIL_PASSWORD: str
  MAIL_SERVER: str
  MAIL_PORT: str

  @property
  def IPOS_DB_URL(self):
    return f"postgresql://{self.IPOS_DB_USERNAME}:{self.IPOS_DB_PASSWORD}@{self.IPOS_DB_HOST}:{self.IPOS_DB_PORT}/{self.IPOS_DB_NAME}"

  @property
  def APP_DB_URL(self):
    return f"postgresql://{self.APP_DB_USERNAME}:{self.APP_DB_PASSWORD}@{self.APP_DB_HOST}:{self.APP_DB_PORT}/{self.APP_DB_NAME}"

  class Config:
    env_file = ".env"

settings = Settings()