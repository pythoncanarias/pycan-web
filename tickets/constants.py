class PAYMENT_METHOD:
    STRIPE = 1
    BANK_TRANSFERENCE = 2
    PAYPAL = 3
    CHOICES = (
        (STRIPE, 'Stripe (default)'),
        (BANK_TRANSFERENCE, 'Bank transference'),
        (PAYPAL, 'PayPal'),
    )
