from unittest.mock import MagicMock, patch

import pytest

from src.utils.email_reporting import (
    create_report_email,
    send_report_email,
    share_executive_report,
)


def test_create_report_email():
    message = create_report_email(
        sender="sender@example.com",
        recipient="manager@example.com",
        subject="OnboardIQ Executive Report",
        report="# OnboardIQ Executive Summary Report",
    )

    assert message["From"] == "sender@example.com"
    assert message["To"] == "manager@example.com"
    assert message["Subject"] == "OnboardIQ Executive Report"
    assert "OnboardIQ Executive Summary Report" in message.get_content()


def test_create_report_email_rejects_empty_report():
    with pytest.raises(ValueError, match="report must not be empty"):
        create_report_email(
            sender="sender@example.com",
            recipient="manager@example.com",
            subject="Report",
            report="",
        )


@patch("src.utils.email_reporting.smtplib.SMTP")
def test_send_report_email_without_authentication(mock_smtp):
    smtp = MagicMock()
    mock_smtp.return_value.__enter__.return_value = smtp

    message = create_report_email(
        sender="sender@example.com",
        recipient="manager@example.com",
        subject="Report",
        report="Executive report",
    )

    send_report_email(
        message=message,
        smtp_host="smtp.example.com",
        smtp_port=25,
    )

    mock_smtp.assert_called_once_with(
        "smtp.example.com",
        25,
    )

    smtp.send_message.assert_called_once_with(message)
    smtp.login.assert_not_called()


@patch("src.utils.email_reporting.smtplib.SMTP")
def test_send_report_email_with_authentication(mock_smtp):
    smtp = MagicMock()
    mock_smtp.return_value.__enter__.return_value = smtp

    message = create_report_email(
        sender="sender@example.com",
        recipient="manager@example.com",
        subject="Report",
        report="Executive report",
    )

    send_report_email(
        message=message,
        smtp_host="smtp.example.com",
        smtp_port=587,
        username="user@example.com",
        password="secret",
    )

    smtp.starttls.assert_called_once()
    smtp.login.assert_called_once_with(
        "user@example.com",
        "secret",
    )
    smtp.send_message.assert_called_once_with(message)


@patch("src.utils.email_reporting.send_report_email")
def test_share_executive_report(mock_send):
    share_executive_report(
        report="# Executive Report",
        sender="sender@example.com",
        recipient="manager@example.com",
        subject="OnboardIQ Report",
        smtp_host="smtp.example.com",
        smtp_port=587,
    )

    mock_send.assert_called_once()

    message = mock_send.call_args.kwargs["message"]

    assert message["From"] == "sender@example.com"
    assert message["To"] == "manager@example.com"
    assert message["Subject"] == "OnboardIQ Report"
    assert "Executive Report" in message.get_content()


def test_invalid_smtp_configuration():
    message = create_report_email(
        sender="sender@example.com",
        recipient="manager@example.com",
        subject="Report",
        report="Executive report",
    )

    with pytest.raises(ValueError, match="smtp_host"):
        send_report_email(
            message=message,
            smtp_host="",
            smtp_port=587,
        )
