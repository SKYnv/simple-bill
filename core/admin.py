from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from core.models import User
from accounting.models import Bill
from django.template import loader
from django.urls import reverse
from django.shortcuts import redirect


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
        return loader.render_to_string('admin/unpaid_button.html', {'uuid': instance.uuid})

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(paid_at__isnull=False)


class UserAdmin(SimpleHistoryAdmin):
    list_display = ('_nickname', 'blocked')
    list_filter = ('blocked',)
    inlines = (UnpaidBillInline, PaidBillInline,)

    # a small addition for createsuperuser users
    def _nickname(self, instance):
        if not instance.nickname:
            return '-'
        return instance.nickname

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        mark_unpaid_action = [key for key in list(request.POST.keys()) if key.startswith('mark_unpaid__')]

        if not mark_unpaid_action:
            return super().changeform_view(request, object_id, form_url, extra_context)
        else:
            bill_uuid = mark_unpaid_action[0].replace('mark_unpaid__', '')
            Bill.objects.filter(uuid=bill_uuid).update(paid_at=None)
            return redirect(
                reverse('admin:core_user_change', args=(object_id,))
            )


admin.site.register(User, UserAdmin)
