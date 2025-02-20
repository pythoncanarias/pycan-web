class FEE_PAYMENT_TYPE:
    BANK_TRANSFERENCE = 'BT'
    STRIPE = 'ST'
    PAYPAL = 'PP'
    CHOICES = (
        (BANK_TRANSFERENCE, 'Transferencia bancaria'),
        (STRIPE, 'Stripe'),
        (PAYPAL, 'PayPal')
    )


class FEE_AMOUNT:
    GENERAL = 20
    STUDENT = 10
    CHOICES = (
        (GENERAL, 'General'),
        (STUDENT, 'Estudiante y/o Desempleado')
    )


# days for default membership period
DEFAULT_MEMBERSHIP_PERIOD = 365

# days por default position period
DEFAULT_POSITION_PERIOD = 4 * 365
