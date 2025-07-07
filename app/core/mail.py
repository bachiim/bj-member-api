from fastapi_mail import ConnectionConfig, FastMail

from .config import settings

mail_config = ConnectionConfig(
  MAIL_USERNAME=settings.MAIL_USERNAME,
  MAIL_PASSWORD=settings.MAIL_PASSWORD,
  MAIL_FROM=settings.MAIL_USERNAME,
  MAIL_PORT=settings.MAIL_PORT,
  MAIL_SERVER=settings.MAIL_SERVER,
  MAIL_FROM_NAME="BJ Member",
  MAIL_STARTTLS=True,
  MAIL_SSL_TLS=False,
  USE_CREDENTIALS=True,
  VALIDATE_CERTS=True
)

fastmail = FastMail(mail_config)