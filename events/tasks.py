import base64
import io
import os
import shutil

import pyqrcode
import sendgrid
from django.conf import settings
from django.template import loader
from django.utils import timezone
from django_rq import job
from sendgrid.helpers.mail import Attachment, Content, Email, Mail

from commons.filters import as_markdown
from libs.reports.core import Report


def get_qrcode_as_svg(text, scale=8):
    img = pyqrcode.create(str(text))
    buff = io.BytesIO()
    img.svg(buff, scale=scale)
    return buff.getvalue().decode('ascii')


def get_tickets_dir():
    _dir = os.path.join(settings.BASE_DIR, 'temporal', 'tickets')
    if not os.path.isdir(_dir):
        os.makedirs(_dir)
    return _dir


def create_ticket_pdf(ticket, force=False):
    output_dir = get_tickets_dir()
    pdf_file = 'ticket-{}.pdf'.format(ticket.keycode)
    full_name = os.path.join(output_dir, pdf_file)
    if not os.path.exists(full_name) or force:
        event = ticket.article.event
        qr_code = get_qrcode_as_svg(ticket.keycode, scale=6)
        report = Report('events/ticket.j2', {
            'ticket': ticket,
            'event': event,
            'qr_code': qr_code,
        })
        report.render(http_response=False)
        shutil.move(report.template_pdf.name, full_name)
    return full_name


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
    pdf_filename = create_ticket_pdf(ticket)
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
    if force:
        create_ticket_pdf(ticket, force=True)
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
