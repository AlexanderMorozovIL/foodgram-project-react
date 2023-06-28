from django.contrib import admin

from .models import CustomUser, Subscription


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = ('email', 'first_name')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Subscription)
