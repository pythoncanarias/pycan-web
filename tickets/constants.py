class PAYMENT_METHOD:
    STRIPE = 1
    BANK_TRANSFERENCE = 2
    PAYPAL = 3
    SUMUP = 4
    CHOICES = (
        (STRIPE, 'Stripe (default)'),
        (BANK_TRANSFERENCE, 'Bank transference'),
        (PAYPAL, 'PayPal'),
        (SUMUP, 'SumUp'),
    )
