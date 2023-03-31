from django.contrib import admin
from users.models import User
from users.models import Subscribe


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "pk",
        "email",
        "first_name",
        "last_name",
    )
    search_fields = (
        "username",
        "email",
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
