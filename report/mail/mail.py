import os
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import smtplib

EMAIL_SENDER = "torgerboc@gmail.com"

def format_receivers(receivers) -> str:
    if not isinstance(receivers, str) and not isinstance(receivers, list):
        raise ValueError("Receivers must be a string or a list of strings.")
    if isinstance(receivers, str) and "\n" in receivers:
        return receivers.replace("\n", ", ")
    if isinstance(receivers, list):
        return ", ".join(receivers)
    return receivers

def receiver_emails(filepath: str = "receivers.txt") -> str:
    with open(filepath, "r") as f:
        return format_receivers(f.read())

def attach_pdf(email: EmailMessage, pdf_path: str) -> None:
    with open(pdf_path, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
    attach.add_header('Content-Disposition', 'attachment', filename=pdf_path)
    email.attach(attach)

def send_email(body: str, receivers: str = None, subject: str = "Weekly Report", 
               pdf_path: str = "../../report.pdf") -> None:
    sender = EMAIL_SENDER
    email = MIMEMultipart()
    email["from"] = sender
    email["to"] = format_receivers(receivers) if receivers else receiver_emails()
    email["subject"] = subject
    email.attach(MIMEText(body, "plain"))

    attach_pdf(email, pdf_path)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender, os.environ.get("EMAIL_PASSWORD"))
        server.send_message(email)
        print("Email sent successfully.")

