import logging

from django.shortcuts import render

from . import breadcrumbs

logger = logging.getLogger(__name__)


def legal_notice(request):
    return render(request, 'legal/legal-notice.html', {
        'title': 'Aviso legal',
        'breadcrumbs': breadcrumbs.bc_root(),
        })


def coc(request, language='es'):
    return render(request, 'legal/coc-es.html', {
        'title': 'Código de conducta',
        'breadcrumbs': breadcrumbs.bc_coc('es'),
        })


def coc_english(request, language='es'):
    return render(request, 'legal/coc-en.html', {
        'title': 'Code of Conduct',
        'breadcrumbs': breadcrumbs.bc_coc(language),
        })



def privacy_policy(request):
    return render(request, 'legal/privacy-policy.html', {
        'title': 'Política de privacidad y protección de datos',
        'breadcrumbs': breadcrumbs.bc_privacy_policy(),
        })


def purchase_terms(request):
    return render(request, 'legal/purchase-terms.html', {
        'title': 'Condiciones generales de compra',
        'breadcrumbs': breadcrumbs.bc_purchase_terms(),
        })


def cookie_policy(request):
    return render(request, 'legal/cookie-policy.html', {
        'title': 'Política de cookies',
        'breadcrumbs': breadcrumbs.bc_cookie_policy(),
        })
