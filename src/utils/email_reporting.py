"""Utilities for sharing OnboardIQ executive reports by email."""

from __future__ import annotations

import smtplib
from email.message import EmailMessage


def create_report_email(
    sender: str,
    recipient: str,
    subject: str,
    report: str,
) -> EmailMessage:
    """Create an email containing an executive report.

    Args:
        sender: Email address of the sender.
        recipient: Email address of the recipient.
        subject: Email subject.
        report: Executive report content.

    Returns:
        Configured EmailMessage.

    Raises:
        ValueError: If a required value is empty.
    """
    if not sender.strip():
        raise ValueError("sender must not be empty.")

    if not recipient.strip():
        raise ValueError("recipient must not be empty.")

    if not subject.strip():
        raise ValueError("subject must not be empty.")

    if not report.strip():
        raise ValueError("report must not be empty.")

    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject

    message.set_content(report)

    return message


def send_report_email(
    message: EmailMessage,
    smtp_host: str,
    smtp_port: int,
    username: str | None = None,
    password: str | None = None,
) -> None:
    """Send an executive report through an SMTP server.

    Authentication is performed only when both username and
    password are supplied.

    Args:
        message: EmailMessage to send.
        smtp_host: SMTP server hostname.
        smtp_port: SMTP server port.
        username: Optional SMTP username.
        password: Optional SMTP password.
    """
    if not isinstance(message, EmailMessage):
        raise TypeError("message must be an EmailMessage.")

    if not smtp_host.strip():
        raise ValueError("smtp_host must not be empty.")

    if smtp_port <= 0:
        raise ValueError("smtp_port must be greater than zero.")

    with smtplib.SMTP(smtp_host, smtp_port) as smtp:
        smtp.ehlo()

        if username is not None and password is not None:
            smtp.starttls()
            smtp.ehlo()
            smtp.login(username, password)

        smtp.send_message(message)


def share_executive_report(
    report: str,
    sender: str,
    recipient: str,
    subject: str,
    smtp_host: str,
    smtp_port: int,
    username: str | None = None,
    password: str | None = None,
) -> None:
    """Create and send an executive report email."""
    message = create_report_email(
        sender=sender,
        recipient=recipient,
        subject=subject,
        report=report,
    )

    send_report_email(
        message=message,
        smtp_host=smtp_host,
        smtp_port=smtp_port,
        username=username,
        password=password,
    )
