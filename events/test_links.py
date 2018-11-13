import pytest
from events import links


def test_ticket_purchase():
    assert links.ticket_purchase(9) == '/events/ticket/purchase/9/'


def test_ticket_purchase_needs_an_integer():
    with pytest.raises(TypeError):
        links.ticket_purchase(None)


def test_article_bought():
    assert links.article_bought(9) == '/events/ticket/purchase/bought/9/'


def test_trade():
    sell_code = 'f67b4b1a-87eb-40a5-8855-d3167c4de403'
    buy_code = '1cc0e40a-adcc-4ca5-89f2-d84d8b994ff9'
    tgt = '/events/abc/trade/{}/{}/'.format(sell_code, buy_code)
    url = links.trade('abc', sell_code, buy_code)
    assert url == tgt


if __name__ == '__main__':
    pytest.main()
