from libs.reports.core import Report


def send_ticket(email, ticket):
    r = Report('events/ticket.j2', {
        'ticket': ticket,
        'qrcode_url': ticket.get_qrcode_url(),
    })
    r.render(http_response=False)
    print(r.template_pdf.name)

