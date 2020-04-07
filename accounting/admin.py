from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from accounting.models import Bill


class BillAdmin(SimpleHistoryAdmin):
    pass


admin.site.register(Bill, BillAdmin)
