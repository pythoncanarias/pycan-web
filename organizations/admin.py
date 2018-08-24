from django.contrib import admin

from .models import Organization, OrganizationSubcategory, \
    OrganizationCategory, Membership


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass


@admin.register(OrganizationSubcategory)
class OrganizationSubcategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'code': ('name', ), }


@admin.register(OrganizationCategory)
class OrganizationCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'code': ('name', ), }


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    pass
