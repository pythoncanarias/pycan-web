import pytest
from events import links


def test_ticket_purchase():
    assert links.ticket_purchase(9) == '/events/ticket/purchase/9/'


def test_ticket_purchase_needs_an_integer():
    with pytest.raises(TypeError):
        links.ticket_purchase(None)

def test_ticket_purchase():
    assert links.ticket_purchase(9) == '/events/ticket/purchase/9/'


def test_article_bought():
    assert links.article_bought(9) == '/events/ticket/purchase/bought/9/'


if __name__ == '__main__':
    pytest.main()

