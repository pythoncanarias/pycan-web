import stripe
import pytest
from . import stripe_utils


def test_get_description_from_exception_card_error():
    exp = stripe.error.CardError('Message', 'Param', 'Code')
    msg, extra_info = stripe_utils.get_description_from_exception(exp)
    assert msg == 'Ha habido un problema al procesar la tarjeta'
    assert extra_info == ''


def test_get_description_from_exception_rate_limit_error():
    exp = stripe.error.RateLimitError('Message', 'Param', 'Code')
    msg, extra_info = stripe_utils.get_description_from_exception(exp)
    assert msg == 'Se han hecho demasiadas peticiones en muy poco tiempo'
    assert extra_info == ''


def test_get_description_from_exception_authentication_error():
    exp = stripe.error.AuthenticationError('Message', 'Param', 'Code')
    msg, extra_info = stripe_utils.get_description_from_exception(exp)
    assert msg == 'La autenticación con Stripe ha fallado'
    assert extra_info == '¿Se han definido correctamante las credencias?'


def test_get_description_from_exception_api_connection_error():
    exp = stripe.error.APIConnectionError('Message', 'Param', 'Code')
    msg, extra_info = stripe_utils.get_description_from_exception(exp)
    assert msg == 'La comunicacion con los servidores de Stripe ha fallado'
    assert extra_info == ''


def test_get_description_from_exception_stripe_error():
    exp = stripe.error.StripeError('Message', 'Param', 'Code')
    msg, extra_info = stripe_utils.get_description_from_exception(exp)
    assert msg == 'Ha habido un exception con el servicio de Stripe'
    assert extra_info == ''


def test_get_description_from_exception_others():
    exp = Exception('General exception')
    msg, extra_info = stripe_utils.get_description_from_exception(exp)
    assert msg == 'Ha habido un error al procesar su pago'
    assert extra_info == ''


if __name__ == '__main__':
    pytest.main()
