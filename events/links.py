from django.urls import reverse


def event_detail(slug):
    return reverse('events:detail_event', kwargs={'slug': slug})


def ticket_purchase(pk):
    pk = int(pk)
    return reverse('events:ticket_purchase', kwargs={'id_article': pk})
