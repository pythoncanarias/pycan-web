import logging

from django.shortcuts import render

from .models import FAQItem

logger = logging.getLogger(__name__)


def faq_list(request):
    faqs = FAQItem.objects.order_by('id')
    return render(request, 'faq/faq_list.html', {'faqs': faqs})
