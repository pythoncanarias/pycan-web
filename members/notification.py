import os

import sendgrid
from django.conf import settings
from django.template import loader
from django_rq import job
from sendgrid.helpers.mail import Content, Email, Mail

from commons.filters import as_markdown


def create_invitation_message(key, first_name, last_name, email):
    tmpl = loader.get_template('members/email/invitation_message.md')
    subject = f'Bienvenido/a {first_name} a Python Canarias'
    body = tmpl.render({
        'key': key,
        'first_name': first_name,
        'last_name': last_name,
        'email': email
    })
    mail = Mail(
        from_email=Email(settings.CONTACT_EMAIL, settings.ASSOCIATION_NAME),
        subject=subject,
        to_email=Email(email),
        content=Content('text/html', as_markdown(body)))
    return mail


@job
def send_invitation(key, first_name, last_name, email):
    msg = create_invitation_message(key, first_name, last_name, email)
    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
    response = sg.client.mail.send.post(request_body=msg.get())
    if response.status_code >= 400:
        error_msg = []
        error_msg.append('STATUS CODE: {}'.format(response.status_code))
        error_msg.append('RESPONSE HEADERS: {}'.format(response.headers))
        error_msg.append('RESPONSE BODY: {}'.format(response.body))
        raise Exception(os.linesep.join(error_msg))
