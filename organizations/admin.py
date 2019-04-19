from django.contrib import admin
from django.http import HttpResponse

from .models import (Membership, Organization, OrganizationCategory,
                     OrganizationRole)


class MembershipInline(admin.StackedInline):
    model = Membership
    extra = 0
    autocomplete_fields = ['organization']
    fk_name = 'organization'


class OrganizationCategoryInline(admin.StackedInline):
    model = OrganizationCategory
    extra = 0


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    inlines = [MembershipInline]
    search_fields = ['name']
    list_display = ('name', 'url', 'memberships')
    list_filter = ('memberships__event', )

    def memberships(self, obj):
        return (', '.join('[{}] {}'.format(x.event, x.category)
                          for x in obj.memberships.all()))


@admin.register(OrganizationRole)
class OrganizationRoleAdmin(admin.ModelAdmin):
    inlines = [OrganizationCategoryInline]
    prepopulated_fields = {'code': ('name', ), }
    list_display = ('name', 'code', 'display_name')


@admin.register(OrganizationCategory)
class OrganizationCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'code': ('name', ), }
    list_display = ('name', 'role', 'code', 'display_name')


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('event', 'organization', 'category', 'amount', 'order')
    list_filter = ('category__name',)
    search_fields = ['organization__name']
    autocomplete_fields = ['organization', 'joint_organization']

    def download_emails(self, request, queryset):
        content = ','.join([m.get_email() for m in queryset])
        filename = 'emails.txt'
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={}'.format(
            filename)
        return response

    download_emails.short_description = 'Download management emails'

    actions = [download_emails, ]
