import stripe


def get_description_from_exception(exp):
    extra_info = ''
    if isinstance(exp, stripe.error.CardError):
        msg = 'Ha habido un problema al procesar la tarjeta'
    elif isinstance(exp, stripe.error.RateLimitError):
        msg = 'Se han hecho demasiadas peticiones en muy poco tiempo'
    elif isinstance(exp, stripe.error.InvalidRequestError):
        msg = 'Se han pasado parámetros incorrectos a la API de Stripe'
    elif isinstance(exp, stripe.error.AuthenticationError):
        msg = 'La autenticación con Stripe ha fallado'
        extra_info = '¿Se han definido correctamante las credencias?'
    elif isinstance(exp, stripe.error.APIConnectionError):
        msg = 'La comunicacion con los servidores de Stripe ha fallado'
    elif isinstance(exp, stripe.error.StripeError):
        msg = 'Ha habido un exception con el servicio de Stripe'
    else:  # Some other kind of non-stripe exceptions
        msg = 'Ha habido un error al procesar su pago'
    return msg, extra_info
