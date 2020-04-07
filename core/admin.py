from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from core.models import User


class UserAdmin(SimpleHistoryAdmin):
    pass


admin.site.register(User, UserAdmin)
