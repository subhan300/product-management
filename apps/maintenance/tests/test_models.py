import pytest
from django.utils import timezone
from apps.maintenance.models import Maintenance, KanbanColumn, MaintenanceDetail, Message

@pytest.mark.django_db
class TestMaintenanceModel:
    def test_create_maintenance(self):
        maintenance = Maintenance.objects.create(
            title="Test Maintenance",
            enquiryDate=timezone.now(),
            user_id=1,  # Replace with a valid user ID
        )
        assert maintenance.title == "Test Maintenance"
        assert maintenance.enquiryDate is not None
        assert maintenance.user_id == 1

    # Add more tests for Maintenance model fields and methods here

@pytest.mark.django_db
class TestKanbanColumnModel:
    def test_create_kanban_column(self):
        column = KanbanColumn.objects.create(
            name="Test Column",
            status_code="test",
            order=1,
        )
        assert column.name == "Test Column"
        assert column.status_code == "test"
        assert column.order == 1

    # Add more tests for KanbanColumn model fields and methods here

@pytest.mark.django_db
class TestMaintenanceDetailModel:
    def test_create_maintenance_detail(self):
        maintenance = Maintenance.objects.create(
            title="Test Maintenance",
            enquiryDate=timezone.now(),
            user_id=1,
        )
        detail = MaintenanceDetail.objects.create(
            problemTitle="Test Issue",
            problemDescription="Test description",
            maintenance=maintenance,
        )
        assert detail.problemTitle == "Test Issue"
        assert detail.problemDescription == "Test description"
        assert detail.maintenance_id == maintenance.id

    # Add more tests for MaintenanceDetail model fields and methods here

@pytest.mark.django_db
class TestMessageModel:
    def test_create_message(self):
        maintenance = Maintenance.objects.create(
            title="Test Maintenance",
            enquiryDate=timezone.now(),
            user_id=1,
        )
        message = Message.objects.create(
            message="Test Message",
            maintenance=maintenance,
            user_id=1,
        )
        assert message.message == "Test Message"
        assert message.maintenance_id == maintenance.id
        assert message.user_id == 1

    # Add more tests for Message model fields and methods here
