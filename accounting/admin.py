from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from accounting.models import Bill
from django.utils import timezone
from django import forms
from django.conf import settings


class BillMetadataAdminForm(forms.ModelForm):
    type = forms.ChoiceField(choices=(('card', 'card'), ('cash', 'cash')))
    code = forms.CharField(required=False)
    url = forms.URLField(required=False)
    _amount = forms.FloatField(required=False)

    metadata = {}

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        try:
            type = self.instance.metadata.get('type')
            self.fields['type'].initial = type
            self.fields['code'].initial = self.instance.metadata.get('code', '')
            self.fields['url'].initial = self.instance.metadata.get('url', '')
            self.fields['_amount'].initial = self.instance.metadata.get('amount', '')

            if type == 'card':
                self.fields['_amount'].widget = forms.HiddenInput()
            else:
                self.fields['code'].widget = forms.HiddenInput()
                self.fields['url'].widget = forms.HiddenInput()
        except:
            pass

    class Meta:
        model = Bill
        fields = ('amount', 'due', 'paid_at', 'user', 'type', 'code', 'url', '_amount')

    def save(self, commit=True):
        self.instance.metadata = self.metadata
        return super().save(commit=commit)

    def clean(self):
        self.metadata = {}
        cleaned_data = super().clean()
        _type = cleaned_data.pop('type')

        if _type == 'card':
            self.metadata['code'] = cleaned_data.pop('code')
            self.metadata['url'] = cleaned_data.pop('url')
        else:
            self.metadata['amount'] = cleaned_data.pop('_amount')
        self.metadata['type'] = _type
        return cleaned_data


class PaymentTypeListFilter(admin.SimpleListFilter):
    title = 'payment type'
    parameter_name = 'metadata'

    def lookups(self, request, model_admin):
        return ('card', 'by card'), ('cash', 'by cash')

    def queryset(self, request, queryset):
        if self.value() == 'card':
            return queryset.filter(paid_at__isnull=False, metadata__contains={"type": "card"})
        if self.value() == 'cash':
            return queryset.filter(paid_at__isnull=False, metadata__contains={"type": "cash"})


class PaidStatusListFilter(admin.SimpleListFilter):
    title = 'paid status'
    parameter_name = 'paid_at'

    def lookups(self, request, model_admin):
        return ('paid', 'paid'), ('not_paid', 'not paid')

    def queryset(self, request, queryset):
        if self.value() == 'paid':
            return queryset.filter(paid_at__isnull=False)
        if self.value() == 'not_paid':
            return queryset.filter(paid_at__isnull=True)


class PaidTimeListFilter(admin.SimpleListFilter):
    title = 'paid time'
    parameter_name = 'due'

    def lookups(self, request, model_admin):
        return ('today', 'today'),

    def queryset(self, request, queryset):
        if self.value() == 'today':
            return queryset.filter(paid_at__isnull=True, due__day=timezone.now().day)


class BillAdmin(SimpleHistoryAdmin):
    list_filter = (PaidStatusListFilter, PaidTimeListFilter, PaymentTypeListFilter)
    list_display = ('uuid', 'amount', 'due', 'paid_at', 'user', '_payment_type')

    fieldsets = ((None,
                  {'fields': ('amount', 'due', 'paid_at', 'user')}),
                 ('Metadata',
                  {'fields': ('type', 'code', 'url', '_amount')}))

    form = BillMetadataAdminForm

    def _payment_type(self, instance):
        return instance.metadata.get('type')

    def save_model(self, request, obj, form, change):
        user = request.user
        if float(request.POST.get('amount_0')) >= settings.ADD_AMOUNT_LIMIT:
            obj.amount = 0
            user.note += f'\nAttempt to set amount >= {settings.ADD_AMOUNT_LIMIT} to bill: {obj}'
            user.save()
        super().save_model(request, obj, form, change)


admin.site.register(Bill, BillAdmin)
