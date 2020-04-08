from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from core.models import User
from accounting.models import Bill
from django.utils.safestring import mark_safe
from django.template import loader
from django.urls import re_path, reverse
from django.utils.html import format_html


class BillInline(admin.TabularInline):
    model = Bill
    readonly_fields = ('payment_type', )
    list_display = ('payment_type',)
    exclude = ('metadata', 'paid_at', 'due')
    extra = 0
    can_delete = False

    def payment_type(self, instance):
        return instance.metadata.get('type')


class UnpaidBillInline(BillInline):
    verbose_name = 'Unpaid bill'
    verbose_name_plural = 'Unpaid bills'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(paid_at__isnull=True)


class PaidBillInline(BillInline):
    verbose_name = 'Paid bill'
    verbose_name_plural = 'Paid bills'
    readonly_fields = ('payment_type', 'mark_unpaid')
    list_display = ('payment_type', 'mark_unpaid')

    def mark_unpaid(self, instance):
        # TODO 'admin/unpaid_button.html' + code
        return mark_safe('<a class="button" href={}>mark unpaid</a>'.format('http://todo'))

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(paid_at__isnull=False)


class UserAdmin(SimpleHistoryAdmin):
    list_display = ('_nickname', 'blocked')
    list_filter = ('blocked',)
    inlines = (UnpaidBillInline, PaidBillInline,)

    # a small addition
    def _nickname(self, instance):
        if not instance.nickname:
            return '-'
        return instance.nickname


admin.site.register(User, UserAdmin)
