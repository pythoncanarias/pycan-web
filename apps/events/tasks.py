import sys

from django.conf import settings
from django.utils import timezone
from django_rq import job

from adapters.emailer import create_message, send_message
from apps.events.models import Proposal
from apps.tickets.models import Ticket


def create_ticket_message(ticket):
    event = ticket.article.event
    pdf_filename = ticket.as_pdf()
    msg = create_message(
        [ticket.customer_email],
        f"Entrada para {event}",
        'events/email/ticket_message.md',
        attachments=[pdf_filename],
        ticket=ticket,
        article=ticket.article,
        category=ticket.article.category,
        event=event,
        )
    return msg


@job
def send_ticket(id_ticket, force=False):
    ticket = Ticket.load_ticket(id_ticket)
    ticket.as_pdf(force)
    msg = create_ticket_message(ticket)
    if send_message(msg):
        ticket.send_at = timezone.now()
        ticket.save()
    else:
        print("El subsistema de correo fallo", file=sys.stderr)


# --[ Call for papers ]------------------------------------------------


def create_proposal_acknowledge(id_proposal):
    proposal = Proposal.load_proposal(id_proposal)
    msg = create_message(
        [proposal.email],
        f"Acuse de recibo de su propuesta para {proposal.event}",
        "events/email/proposal_acknowledge.md",
        event=proposal.event,
        proposal=proposal,
        )
    return msg


@job
def send_proposal_acknowledge(id_proposal):
    proposal = Proposal.load_proposal(id_proposal)
    msg = create_proposal_acknowledge(proposal)
    send_message(msg)


def create_proposal_notification(proposal):
    event = proposal.event
    msg = create_message(
        [settings.CONTACT_EMAIL],
        f"Nueva propuesta para {event}",
        'events/email/proposal_notification.md',
        event=proposal.event,
        proposal=proposal,
        )
    return msg


@job
def send_proposal_notification(proposal):
    msg = create_proposal_notification(proposal)
    send_message(msg)
