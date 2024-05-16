
import pytest
from apps.accounts.models import CustomUser


@pytest.fixture
def user(self):
    return CustomUser.objects.create(
        email="testuser@example.com",
        password="testpassword",
    )
