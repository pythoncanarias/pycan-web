class MEMBER_POSITION:
    PRESIDENT = 'PRE'
    VICEPRESIDENT = 'VPR'
    SECRETARY = 'SEC'
    TREASURER = 'TRE'
    CHAIR1 = 'CH1'
    CHAIR2 = 'CH2'
    CHAIR3 = 'CH3'
    CHAIR4 = 'CH4'
    CHOICES = (
        (PRESIDENT, 'Presidencia'),
        (VICEPRESIDENT, 'Vicepresidencia'),
        (SECRETARY, 'Secretaría'),
        (TREASURER, 'Tesorería'),
        (CHAIR1, 'Vocalía 1'),
        (CHAIR2, 'Vocalía 2'),
        (CHAIR3, 'Vocalía 3'),
        (CHAIR4, 'Vocalía 4')
    )


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
