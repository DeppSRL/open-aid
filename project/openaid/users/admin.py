from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _

from .models import User


class RecipientSetInline(admin.TabularInline):
    model = User.recipient_set.through
    extra = 0

class UserAdmin(AuthUserAdmin):

    list_display = ('username', 'email', 'nation', 'city', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')

    inlines = [
        RecipientSetInline,
    ]


admin.site.register(User, UserAdmin)