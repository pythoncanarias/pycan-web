from django.shortcuts import render

from . import models
from . import breadcrumbs


def list_active_job_offers(request):
    jobs = models.JobOffer.actives.all().order_by('-id')
    return render(request, 'jobs/list_jobs.html', {
        "title": "Empleo - Ofertas laborales",
        "breadcrumbs": breadcrumbs.bc_root(),
        "jobs": jobs,
    })
