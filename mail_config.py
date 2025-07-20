from fastapi_mail import FastMail, ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME = "dasha.komzolova.0615@gmail.com",
    MAIL_PASSWORD = "oirf pycv ioic xjpo",  # ⬅️ Тут вставь Gmail App Password!
    MAIL_FROM = "dasha.komzolova.0615@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS=True,  # ⬅️ правильно!
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS = True
)

fast_mail = FastMail(conf)
