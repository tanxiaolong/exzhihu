from threading import Thread
from flask import render_template
from flask_mail import Message
from app import mail
from manage import app

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.html = render_template(template, **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr