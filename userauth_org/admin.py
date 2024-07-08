from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Organizations
from .forms import AdminChangeForm


# Register your models here.

class UserAdmin(BaseUserAdmin):
    model = User
    search_fields = ['firstname', 'lastname', 'phone', 'email']
    ordering = ['created']
    list_display = ['firstname', 'lastname']
    list_filter = ['is_superuser']

    form = AdminChangeForm

    fieldsets = (
        (None, {'fields': (['email'])}),
        ('Personal info', {'fields': ('firstname', 'lastname', 'phone')}),
        ('Permissions', {'fields': ('is_superuser', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
        'classes': ('wide',),
        'fields': ('firstname', 'lastname', 'phone','email', 'password1', 'password2'),
        }),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Organizations)