from decimal import Decimal

NO_IGIC = 0
IGIC_7 = 1
IVA_21 = 2
TAX_CHOICES = (
    (NO_IGIC, 'exto IGIC'),
    (IGIC_7, 'IGIC (7%)'),
    (IVA_21, 'iva (21%)'),
)
TAX_MULTIPLIER = {
    NO_IGIC: Decimal('0'),
    IGIC_7: Decimal('7'),
    IVA_21: Decimal('21'),
}
RETENTION_0 = 0
RETENTION_6 = 1
RETENTION_12 = 2
RETENTION_21 = 3
RETENTION_CHOICES = (
    (RETENTION_0, 'NO RETENTION'),
    (RETENTION_6, 'IRPF 6%'),
    (RETENTION_12, 'IRPF 12%'),
    (RETENTION_21, 'IRPF 21%'),
)
RETENTION_MULTIPLIER = {
    RETENTION_0: Decimal('0'),
    RETENTION_6: Decimal('6'),
    RETENTION_12: Decimal('12'),
    RETENTION_21: Decimal('21'),
}
