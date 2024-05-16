import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import CustomUser
from apps.maintenance.models import Maintenance, KanbanColumn
from apps.maintenance.serializers import MaintenanceSerializer
from django.utils import timezone


@pytest.mark.django_db
class TestMaintenanceAPI:
    @pytest.fixture
    def user(self):
        return CustomUser.objects.create_user(
            email="testuser@example.com",
            password="testpassword",
        )

    @pytest.fixture
    def maintenance(self, user):
        return Maintenance.objects.create(
            title="Test Maintenance",
            enquiryDate=timezone.now(),
            user=user,
        )

    def test_get_maintenance_list(self, user, maintenance):
        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse("maintenance-list")
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]["title"] == "Test Maintenance"

    def test_create_maintenance(self, user):
        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse("maintenance-list")
        data = {
            "title": "New Maintenance",
            "enquiryDate": "2023-09-17T12:00:00Z",  # Replace with a valid date
            "user": user.id,
            # Add other required fields here
        }
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    # Add more API tests for maintenance-related endpoints
