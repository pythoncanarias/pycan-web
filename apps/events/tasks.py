import base64
import os

import sendgrid
from django.conf import settings
from django.template import loader
from django.utils import timezone
from django_rq import job
from sendgrid.helpers.mail import Attachment, Content, Email, Mail

from apps.commons.filters import as_markdown


def create_ticket_message(ticket):
    event = ticket.article.event
    tmpl = loader.get_template('events/email/ticket_message.md')
    subject = 'Entrada para {}'.format(event.name)
    body = tmpl.render({
        'ticket': ticket,
        'article': ticket.article,
        'category': ticket.article.category,
        'event': event,
    })
    mail = Mail(
        from_email=Email(settings.CONTACT_EMAIL, settings.ASSOCIATION_NAME),
        subject=subject,
        to_email=Email(ticket.customer_email),
        content=Content('text/html', as_markdown(body)))

    attachment = Attachment()
    pdf_filename = ticket.as_pdf()
    with open(pdf_filename, 'rb') as f:
        data = f.read()
    attachment.content = base64.b64encode(data).decode()
    attachment.type = 'application/pdf'
    attachment.filename = 'ticket.pdf'
    attachment.disposition = 'attachment'
    mail.add_attachment(attachment)
    return mail


@job
def send_ticket(ticket, force=False):
    ticket.as_pdf(force)
    msg = create_ticket_message(ticket)
    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
    response = sg.client.mail.send.post(request_body=msg.get())
    if response.status_code >= 400:
        error_msg = []
        error_msg.append('STATUS CODE: {}'.format(response.status_code))
        error_msg.append('RESPONSE HEADERS: {}'.format(response.headers))
        error_msg.append('RESPONSE BODY: {}'.format(response.body))
        raise Exception(os.linesep.join(error_msg))
    ticket.send_at = timezone.now()
    ticket.save()
