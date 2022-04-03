from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


# Register your models here.
# admin패널에서 models.user를 사용함
# models.User를 컨트롤하는 클래스는 CustomUserAdmin 클래스임
# admin.site.register(models.User, CustomUserAdmin)
# admin.site.register(models.User, CustomUserAdmin)
@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """Custom User Admin"""

    # list_display = ("username", "email", "gender", "language", "currency", "superhost")
    # list_filter = ("gender", "language", "currency", "superhost")
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birthdate",
                    "language",
                    "currency",
                    "login_method",
                    "superhost",
                )
            },
        ),
        # ("cherry", {"fields": ("currency", "birthdate", "language")}),
    )

    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
        "login_method",
    )
