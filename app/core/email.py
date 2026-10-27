import os
import smtplib
import ssl
from dataclasses import dataclass
from email.message import EmailMessage

import certifi
from dotenv import load_dotenv

load_dotenv()


class EmailConfigurationError(RuntimeError):
    pass


class EmailDeliveryError(RuntimeError):
    pass


@dataclass(frozen=True)
class SMTPSettings:
    host: str
    port: int
    sender: str
    username: str | None
    password: str | None
    use_ssl: bool


def get_smtp_settings() -> SMTPSettings:
    host = os.getenv("SMTP_HOST")
    sender = os.getenv("SMTP_FROM_EMAIL")
    if not host or not sender:
        raise EmailConfigurationError(
            "Password reset email is not configured. Set SMTP_HOST and SMTP_FROM_EMAIL."
        )

    try:
        port = int(os.getenv("SMTP_PORT", "587"))
    except ValueError as error:
        raise EmailConfigurationError("SMTP_PORT must be a valid port number.") from error
    if not 1 <= port <= 65535:
        raise EmailConfigurationError("SMTP_PORT must be between 1 and 65535.")

    username = os.getenv("SMTP_USERNAME") or None
    raw_password = os.getenv("SMTP_PASSWORD")
    password = "".join(raw_password.split()) if raw_password else None
    if bool(username) != bool(password):
        raise EmailConfigurationError(
            "Set both SMTP_USERNAME and SMTP_PASSWORD, or leave both empty."
        )

    return SMTPSettings(
        host=host,
        port=port,
        sender=sender,
        username=username,
        password=password,
        use_ssl=os.getenv("SMTP_USE_SSL", "").lower() in {"1", "true", "yes"},
    )


def send_password_reset_email(recipient: str, otp: str, settings: SMTPSettings) -> None:
    message = EmailMessage()
    message["Subject"] = "Your Servix password reset code"
    message["From"] = settings.sender
    message["To"] = recipient
    message.set_content(
        f"Your Servix password reset code is {otp}.\n\n"
        "This code expires in 3 minutes. If you did not request a password reset, "
        "you can ignore this email."
    )

    try:
        tls_context = ssl.create_default_context(cafile=certifi.where())
        if settings.use_ssl:
            with smtplib.SMTP_SSL(
                settings.host,
                settings.port,
                timeout=15,
                context=tls_context,
            ) as smtp:
                if settings.username and settings.password:
                    smtp.login(settings.username, settings.password)
                smtp.send_message(message)
        else:
            with smtplib.SMTP(settings.host, settings.port, timeout=15) as smtp:
                smtp.ehlo()
                smtp.starttls(context=tls_context)
                smtp.ehlo()
                if settings.username and settings.password:
                    smtp.login(settings.username, settings.password)
                smtp.send_message(message)
    except (OSError, smtplib.SMTPException) as error:
        raise EmailDeliveryError("Could not deliver password reset email.") from error
