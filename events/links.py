from django.urls import reverse


def ticket_purchase(pk):
    pk = int(pk)
    return reverse('events:ticket_purchase', kwargs={'id_article': pk})
