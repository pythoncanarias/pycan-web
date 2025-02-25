import pytest

from apps.events import links


def test_to_ticket_purchase():
    assert links.to_ticket_purchase(9) == '/events/ticket/purchase/9/'


def test_ticket_purchase_needs_an_integer():
    with pytest.raises(TypeError):
        links.to_ticket_purchase(None)


def test_to_article_bought():
    assert links.to_article_bought(9) == '/events/ticket/purchase/bought/9/'


def test_to_waiting_list_accepted():
    assert links.to_waiting_list_accepted('matraka') == '/events/matraka/waiting-list/accepted/'


def test_to_refund():
    assert links.to_refund('matraka') == '/events/matraka/refund/'


def test_to_refund_accepted():
    assert links.to_refund_accepted('matraka', 4238) == '/events/matraka/refund/accepted/4238/'


def test_to_resend_ticket():
    assert links.to_resend_ticket('matraka') == '/events/matraka/resend_ticket/'


def test_to_resend_confirmation():
    expected = '/events/matraka/resend_ticket/confirmation/'
    assert links.to_resend_confirmation('matraka') == expected


if __name__ == '__main__':
    pytest.main()
