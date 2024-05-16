import pytest
from django.core.exceptions import ValidationError
from apps.accounts.models import CustomUser

@pytest.mark.django_db
class TestCustomUserModel:
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="testpassword",
        )
        assert user.email == "testuser@example.com"
        assert user.check_password("testpassword")

    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(
            email="admin@example.com",
            password="adminpassword",
        )
        assert superuser.email == "admin@example.com"
        assert superuser.is_staff
        assert superuser.is_superuser

    def test_invalid_email(self):
        with pytest.raises(ValidationError):
            CustomUser.objects.create_user(email="invalid_email", password="testpassword")
