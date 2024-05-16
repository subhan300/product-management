import pytest
from django.urls import reverse
from django.test import RequestFactory
from apps.accounts.models import CustomUser
from apps.accounts.views import ProfileView, UserLoginView

@pytest.mark.django_db
class TestUserLoginView:
    def test_user_login(self, user):
        factory = RequestFactory()
        request = factory.post(reverse("login"), data={"email": user.email, "password": "testpassword"})
        view = UserLoginView.as_view()
        response = view(request)
        assert response.status_code == 302
        assert response.url == reverse("dashboard")

    def test_user_login_invalid_credentials(self, user):
        factory = RequestFactory()
        request = factory.post(reverse("login"), data={"email": user.email, "password": "wrongpassword"})
        view = UserLoginView.as_view()
        response = view(request)
        assert response.status_code == 200
        assert "Invalid email/password combination." in str(response.content)

@pytest.mark.django_db
class TestProfileView:
    def test_profile_view_authenticated(self):
        user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="testpassword",
        )
        factory = RequestFactory()
        request = factory.get(reverse("profile"))
        request.user = user
        view = ProfileView.as_view()
        response = view(request)
        assert response.status_code == 200
        assert "Profile" in str(response.content)

    def test_profile_view_unauthenticated(self):
        factory = RequestFactory()
        request = factory.get(reverse("profile"))
        view = ProfileView.as_view()
        response = view(request)
        assert response.status_code == 302
        assert response.url == reverse("login")
