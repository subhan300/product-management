import pytest
from django.urls import reverse
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from apps.maintenance.models import Maintenance, KanbanColumn
from apps.maintenance.views import DashboardView, MaintenanceView

User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(
        email="testuser@example.com",
        password="testpassword",
    )

@pytest.mark.django_db
class TestDashboardView:
    def test_dashboard_view_authenticated(self, user):
        factory = RequestFactory()
        request = factory.get(reverse("dashboard"))
        request.user = user
        view = DashboardView.as_view()
        response = view(request)
        assert response.status_code == 200
        assert "Dashboard" in str(response.content)

    def test_dashboard_view_unauthenticated(self):
        factory = RequestFactory()
        request = factory.get(reverse("dashboard"))
        view = DashboardView.as_view()
        response = view(request)
        assert response.status_code == 302
        assert response.url == reverse("login")

    # Add more tests for DashboardView here

@pytest.mark.django_db
class TestMaintenanceView:
    def test_maintenance_view_authenticated(self, user):
        factory = RequestFactory()
        request = factory.get(reverse("maintenance"))
        request.user = user
        view = MaintenanceView.as_view()
        response = view(request)
        assert response.status_code == 200
        assert "Maintenance" in str(response.content)

    def test_maintenance_view_unauthenticated(self):
        factory = RequestFactory()
        request = factory.get(reverse("maintenance"))
        view = MaintenanceView.as_view()
        response = view(request)
        assert response.status_code == 302
        assert response.url == reverse("login")

    # Add more tests for MaintenanceView here
