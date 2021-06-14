from django.contrib import admin

from .models import Notice, NoticeKind


@admin.register(NoticeKind)
class NoticeKindAdmin(admin.ModelAdmin):
    list_display = ('description', 'code', 'days', 'enabled')
    list_filter = ('enabled',)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'kind',
        'member',
        'send_at',
        'reference_date',
        'status',
    )
    list_filter = (
        'member',
        'kind',
        'reference_date',
    )

    def get_queryset(self, request):
        qs = super(NoticeAdmin, self).get_queryset(request)
        return (
            qs.select_related('kind')
            .select_related('member')
            .select_related('member__user')
        )
