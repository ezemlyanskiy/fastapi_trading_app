import smtplib

from email.message import EmailMessage

from celery import Celery
from src.config import (
    REDIS_HOST,
    REDIS_PORT,
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USER,
    SMTP_PASSWORD,
)

celery = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')


def get_email_dashboard_template(username: str):
    email = EmailMessage()
    email['Subject'] = 'Trading Dashboard Report'
    email['from'] = SMTP_USER
    email['to'] = SMTP_USER
    email.set_content(
        '<div>'
        f'<h1 style="color: red;">Hey there, {username}, here is your report. Check out 😊</h1>'
        '<img src="https://static.vecteezy.com/system/resources/previews/008/295/031/original/custom-relationship'
        '-management-dashboard-ui-design-template-suitable-designing-application-for-android-and-ios-clean-style-app'
        '-mobile-free-vector.jpg" width="600">'
        '</div>',
        subtype='html'
    )
    return email


@celery.task
def send_email_dashboard_report(username: str):
    email = get_email_dashboard_template(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
