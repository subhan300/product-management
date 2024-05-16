from django.contrib.auth.forms import UserChangeForm

from apps.accounts.models import CustomUser


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        exclude = ('date_joined', 'last_login', "role", "is_active", "is_superuser", "staff_status", "last_activity", "active",)