from django.contrib import admin

from .models import Organization, OrganizationSubcategory, \
    OrganizationCategory, Membership


class MembershipInline(admin.StackedInline):
    model = Membership
    extra = 0


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    inlines = [MembershipInline]


@admin.register(OrganizationSubcategory)
class OrganizationSubcategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'code': ('name', ), }


@admin.register(OrganizationCategory)
class OrganizationCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'code': ('name', ), }
