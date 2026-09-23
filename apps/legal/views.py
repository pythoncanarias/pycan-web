from django.shortcuts import render

from django.conf import settings
from . import breadcrumbs


def legal_notice(request):
    return render(request, 'legal/legal-notice.html', {
        'titulo': "Aviso legal",
        'subtitulo': settings.ORGANIZATION_NAME,
        'breadcrumbs': breadcrumbs.bc_legal(),
        })


def privacy_policy(request):
    return render(request, 'legal/privacy-policy.html', {
        'titulo': "Política de privadidad",
        'subtitulo': settings.ORGANIZATION_NAME,
        'breadcrumbs': breadcrumbs.bc_privacy_policy(),
        })



def coc(request, language='es'):
    template = 'legal/coc-{}.html'.format(language)
    titulo = "Código de conducta"
    if language == 'en':
        titulo = "Code of conduct"
    return render(request, template, {
        'titulo': titulo,
        'subtitulo': settings.ORGANIZATION_NAME,
        'breadcrumbs': breadcrumbs.bc_coc(language),
        })


def purchase_terms(request):
    return render(request, 'legal/purchase-terms.html', {
        'titulo': 'Condiciones generales de compra',
        'subtitulo': settings.ORGANIZATION_NAME,
        'breadcrumbs': breadcrumbs.bc_purchase_terms(),
        })


def cookie_policy(request):
    return render(request, 'legal/cookie-policy.html', {
        'titulo': 'Política de cookies',
        'subtitulo': settings.ORGANIZATION_NAME,
        'breadcrumbs': breadcrumbs.bc_cookie_policy(),
        })
