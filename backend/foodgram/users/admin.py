from django.contrib import admin

from users.models import Subscribe
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "first_name",
        "last_name",
        "username",
        "password",
        "email",

    )
    search_fields = (
        "username",
        "email",
    )
    list_editable = (
        "password",
    )
    list_filter = (
        "username",
        "email"
    )


class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "author"
    )
    list_editable = (
        "user",
        "author"
    )


admin.site.register(User, UserAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
