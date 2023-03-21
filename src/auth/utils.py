import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

from jinja2 import Environment, FileSystemLoader

from src.auth.config import auth_config


def get_refresh_token_settings(
    refresh_token: str,
    expired: bool = False,
) -> dict[str, Any]:
    base_cookie = {
        "key": auth_config.REFRESH_TOKEN_KEY,
        "httponly": True,
        "samesite": "none",
        "secure": auth_config.SECURE_COOKIES,
        "domain": auth_config.SITE_DOMAIN,
    }
    if expired:
        return base_cookie

    return {
        **base_cookie,
        "value": refresh_token,
        "max_age": auth_config.REFRESH_TOKEN_EXP,
    }


def send_email(
    template_name: str, receiver_email: str, subject: str, render_data: dict[str, str]
) -> None:
    env = Environment(loader=FileSystemLoader("src/auth/templates"), autoescape=True)
    template = env.get_template(template_name)
    html_content = template.render(render_data)

    msg = MIMEMultipart()
    msg["From"] = auth_config.SENDER_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html"))

    # Create SMTP session for sending the mail
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(
        user=auth_config.SENDER_EMAIL, password=auth_config.SENDER_EMAIL_PASSWORD
    )
    server.sendmail(auth_config.SENDER_EMAIL, receiver_email, msg.as_string())
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
