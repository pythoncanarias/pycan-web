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
    template = 'legal/coc-{}.html'.format(language)
    return render(request, template)


def privacy_policy(request):
    return render(request, 'legal/privacy-policy.html', {
        'title': 'Política de privacidad y protección de datos',
        })


def purchase_terms(request):
    return render(request, 'legal/purchase-terms.html')


def cookie_policy(request):
    return render(request, 'legal/cookie-policy.html')
