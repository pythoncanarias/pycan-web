from apps.commons.breadcrumbs import BreadCrumb

def bc_events():
    return BreadCrumb("Eventos", 'events:index')


def bc_past_events():
    return bc_events().step("Eventos pasados", 'events:past_events')



def bc_event(event):
    return bc_events().step(
        event.name,
        'events:detail_event',
        event=event,
        )


def bc_event_sponsors(event):
    return bc_event(event).step(
        "Patrocinadores",
        'events:sponsors',
        event=event,
        )

def bc_resend_ticket(event):
    return bc_event(event).step(
        'Reenviar ticket',
        'events:resend_ticket',
        event=event,
        )

def bc_event_waiting_list(event):
    return bc_event(event).step(
        "Lista de espera",
        'events:waiting_list',
        event=event,
        )


def bc_event_cfp(event):
    return bc_event(event).step(
        "Call for papers",
        'events:cfp',
        event=event,
        )


def bc_event_cfp_thanks(event):
    return bc_event_cfp(event).step(
        "Gracias por su propuesta",
        'events:thanks',
        event=event,
        )


def bc_event_talks(event):
    return bc_event(event).step(
        'Programa',
        'events:event_talks',
        event=event,
        )


def bc_talk(event, talk):
    return bc_event_talks(event).step(
        talk.title,
        'events:detail_task',
        event=event,
        pk=talk.pk,
        )


def bc_event_location(event):
    return bc_event(event).step(
        'Donde',
        'events:event_location',
        event=event,
        )


def bc_event_speakers(event):
    return bc_event(event).step(
        'Ponentes',
        'events:event_spaekers',
        event=event,
        )

