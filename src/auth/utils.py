import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

from jinja2 import Environment, FileSystemLoader

from src.auth.config import settings
from src.config import settings as global_settings


def get_refresh_token_settings(
    refresh_token: str,
    expired: bool = False,
) -> dict[str, Any]:
    base_cookie = {
        "key": "refreshToken",
        "httponly": True,
        "samesite": "none",
        "secure": settings.SECURE_COOKIES,
    }
    if global_settings.ENVIRONMENT.is_deployed:
        base_cookie["domain"] = settings.SITE_DOMAIN

    if expired:
        return base_cookie

    return {
        **base_cookie,
        "value": refresh_token,
        "max_age": settings.REFRESH_TOKEN_EXPIRES_SECONDS,
    }


def send_email(
    template_name: str, receiver_email: str, subject: str, render_data: dict[str, str]
) -> None:
    env = Environment(loader=FileSystemLoader("src/auth/templates"), autoescape=True)
    template = env.get_template(template_name)
    html_content = template.render(render_data)

    msg = MIMEMultipart()
    msg["From"] = settings.SENDER_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html"))

    # Create SMTP session for sending the mail
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user=settings.SENDER_EMAIL, password=settings.SENDER_EMAIL_PASSWORD)
    server.sendmail(settings.SENDER_EMAIL, receiver_email, msg.as_string())
    server.quit()


def send_activate_email(receiver_email: str, username: str, activate_url: str) -> None:
    TEMPLATE_NAME = "activate_account.html"
    SUBJECT = "Activate Your Account!"
    send_email(
        template_name=TEMPLATE_NAME,
        receiver_email=receiver_email,
        subject=SUBJECT,
        render_data={"username": username, "activate_url": activate_url},
    )


def send_reset_password_email(
    receiver_email: str, username: str, reset_url: str
) -> None:
    TEMPLATE_NAME = "reset_password.html"
    SUBJECT = "Reset your password!"
    send_email(
        template_name=TEMPLATE_NAME,
        receiver_email=receiver_email,
        subject=SUBJECT,
        render_data={"username": username, "reset_url": reset_url},
    )
