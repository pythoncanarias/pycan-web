NO_IGIC = 0
IGIC_7 = 1
IVA_21 = 2
TAX_CHOICES = (
    (NO_IGIC, 'IGIC(7%)'),
    (IGIC_7, 'exto IGIC'),
    (IVA_21, 'iva (21%)'),
)
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

ORG_NAME = 'Python Canarias'
ORG_MOTTO = 'algun motto para la org'
ORG_CIF = 'XXXXXXXXB'
ORG_ADDRESS = 'Ctra This tthat'
ORG_CITY = 'San Cristobal de La Laguna'
ORG_EMAIL = 'info@pythoncanarias.es'
ORG_WEB = 'www.pythoncanarias.es'
