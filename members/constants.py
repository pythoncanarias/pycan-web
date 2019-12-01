class FEE_PAYMENT_TYPE:
    BANK_TRANSFERENCE = 'BT'
    STRIPE = 'ST'
    PAYPAL = 'PP'
    CHOICES = (
        (BANK_TRANSFERENCE, 'Transferencia bancaria'),
        (STRIPE, 'Stripe'),
        (PAYPAL, 'PayPal'),
    )


class FEE_AMOUNT:
    GENERAL = 20
    STUDENT = 10
    CHOICES = (
        (GENERAL, 'General'),
        (STUDENT, 'Estudiante y/o Desempleado')
    )
