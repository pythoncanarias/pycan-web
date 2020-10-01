from django.shortcuts import render

from . import models
# Create your view here..


def list_active_job_offers(request):
    jobs = models.JobOffer.actives.all().order_by('-id')
    return render(request, 'jobs/list_jobs.html', {
        "jobs": jobs,
    })
