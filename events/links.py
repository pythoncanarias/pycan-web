from django.urls import reverse


def event_detail(slug):
    return reverse('events:detail_event', kwargs={'slug': slug})


def ticket_purchase(id_article):
    id_article = int(id_article)
    return reverse('events:ticket_purchase', kwargs={'id_article': id_article})


def article_bought(id_article):
    id_article = int(id_article)
    return reverse('events:article_bought', kwargs={'id_article': id_article})


def waiting_list_accepted(slug):
    return reverse('events:waiting_list_accepted', kwargs={
        'slug': slug,
        })


def trade_success():
    return reverse('events:trade_success')


def trade(sell_code, buy_code):
    return reverse('events:trade', kwargs={
        'sell_code': sell_code,
        'buy_code': buy_code,
        })


def refund(slug):
    return reverse('events:refund', kwargs={
        'slug': slug,
        })


def refund_accepted(slug, pk):
    return reverse('events:refund_accepted', kwargs={
        'slug': slug,
        'pk': pk,
        })
