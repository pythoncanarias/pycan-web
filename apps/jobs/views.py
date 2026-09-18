from django.shortcuts import render
from django.conf import settings

from . import models
from . import breadcrumbs


def list_active_job_offers(request):
    jobs = models.JobOffer.actives.all().order_by('-id')
    return render(request, 'jobs/list_jobs.html', {
        'titulo': f"Ofertas de trabajo - {settings.ORGANIZATION_NAME}",
        'breadcrumbs': breadcrumbs.bc_jobs(),
        "jobs": jobs,
    })
