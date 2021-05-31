from django.contrib import admin

from .models import NoticeKind, Notice


@admin.register(NoticeKind)
class NoticeKindAdmin(admin.ModelAdmin):
    list_display = ('pk', 'app', 'code', 'description',)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'kind',
        'member',
        'reference_date',
        'status',
    )
    list_filter = (
        'member',
        'reference_date',
    )

    def get_queryset(self, request):
        qs = super(NoticeAdmin, self).get_queryset(request)
        return (
            qs
            .select_related('kind')
            .select_related('member')
            .select_related('member__user')
        )


