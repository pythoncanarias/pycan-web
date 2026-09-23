from apps.commons.breadcrumbs import BreadCrumb


def bc_legal():
    return BreadCrumb('Aviso legal', 'legal:legal_notice')


def bc_privacy_policy():
    return bc_legal().step(
        "Política de privacidad",
        'legal:privacy_policy',
        )

def bc_cookie_policy():
    return bc_legal().step(
        "Política de &nbsp;<i>cookies</i>",
        'legal:cookie_policy',
        )


def bc_coc(lang='es'):
    label = "Código de conducta" if lang == 'es' else "Code of conduct"
    return bc_legal().step(
        label,
        'legal:coc',
        )


def bc_purchase_terms():
    return bc_legal().step(
        "Condidiones generales de compra",
        'legal:purchase_terms',
        )

