from django.contrib import admin

from .models import Organization, OrganizationRole, \
    OrganizationCategory, Membership


class MembershipInline(admin.StackedInline):
    model = Membership
    extra = 0
    autocomplete_fields = ['organization']


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
    prepopulated_fields = {'code': ('name', ), }


@admin.register(OrganizationCategory)
class OrganizationCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'code': ('name', ), }
