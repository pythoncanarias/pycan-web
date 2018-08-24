from django.contrib import admin

from .models import Organization, OrganizationSubcategory, \
    OrganizationCategory, Membership


class OrganizationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Organization, OrganizationAdmin)


class OrganizationSubcategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(OrganizationSubcategory, OrganizationSubcategoryAdmin)


class OrganizationCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(OrganizationCategory, OrganizationCategoryAdmin)


class MembershipAdmin(admin.ModelAdmin):
    pass


admin.site.register(Membership, MembershipAdmin)
