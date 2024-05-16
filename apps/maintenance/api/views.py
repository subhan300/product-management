from rest_framework import generics, viewsets, status
from apps.maintenance.models import Company, Building, KanbanColumn, MaintenanceRequest, Message, MaintenanceAssigning, Notification
from apps.maintenance.serializers import (
    CompanySerializer, BuildingSerializer, NotificationSerializer,
)
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from django.shortcuts import get_object_or_404
from apps.accounts.models import CustomUser
from apps.accounts.serializers import ShortUserSerializer, UserSerializer
from django.contrib.auth import get_user_model
from apps.maintenance.models import KanbanColumn, MaintenanceRequest, MaintenanceAssigning, Message
from apps.maintenance.serializers import CreateMessageSerializer, FullKanbanColumnSerializer, MaintenanceSerializer, MessageSerializer, ShortKanbanSerializer
User = get_user_model()


class MaintenanceDetailView(RetrieveAPIView):
    queryset = MaintenanceRequest.objects.filter(is_deleted=False)
    serializer_class = MaintenanceSerializer


class KanbanView(APIView):

    def get(self, request):
        maintenance_columns = KanbanColumn.objects.all().order_by('order')
        serializer = FullKanbanColumnSerializer(maintenance_columns, many=True, context={"request":request})
        return Response(serializer.data)

class CreateMessageView(APIView):
    def get(self, request):
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CreateMessageSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MessageView(APIView):
    def get(self, request, pk):
        messages = Message.objects.filter(maintenance__id=pk).order_by("-created_at")
        print("asdfas")
        serializer = MessageSerializer(messages, many=True)
        return Response({"messages": serializer.data})


class AssignEmployeeView(APIView):
    def post(self, request):
        user = CustomUser.objects.get(id=request.data.get("user"))
        maintenance = request.data.get("maintenance")
        maintenance = MaintenanceRequest.objects.get(id=maintenance, is_deleted=False)
        exist = MaintenanceAssigning.objects.filter(user=user, maintenance=maintenance).first()
        created = False
        if not exist:
            MaintenanceAssigning.objects.create(user=user, maintenance=maintenance)
            if user.role=="tech":
                maintenance.status.status_code = "ip"
                maintenance.save()
            created = True
        return Response({"user": ShortUserSerializer(user).data, "created": created})


class MoveNextView(APIView):
    def post(self, request):
        maintenance_id = request.data.get("maintenance")
        maintenance = get_object_or_404(MaintenanceRequest, id=maintenance_id, is_deleted=False)
        previous_column, next_column = maintenance.move_to_next_status()
        return Response({"nextColumn": ShortKanbanSerializer(next_column).data if next_column else None, "previousColumn": ShortKanbanSerializer(previous_column).data if previous_column else None})

class MovePreviousView(APIView):
    def post(self, request):
        maintenance_id = request.data.get("maintenance")
        maintenance = get_object_or_404(MaintenanceRequest, id=maintenance_id, is_deleted=False)
        previous_column, next_column = maintenance.move_to_previous_status()
        return Response({"previousColumn": ShortKanbanSerializer(previous_column).data if previous_column else None, "nextColumn": ShortKanbanSerializer(next_column).data if next_column else None})


class MoveToView(APIView):
    def post(self, request):
        maintenance_id = request.data.get("maintenance_card_id")
        status_id = request.data.get("kanban_column_id")
        maintenance = get_object_or_404(MaintenanceRequest, id=maintenance_id, is_deleted=False)
        status = get_object_or_404(KanbanColumn, id=status_id )
        maintenance.status = status
        maintenance.save()
        return Response({"message": "Status updated successfully"})


class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # permission_classes = [permissions.IsAuthenticated]

class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    # permission_classes = [permissions.IsAuthenticated]

class CompanyEmployeeListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.filter(role="tech")
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]

# Repeat the above pattern for other models...

# Example for Building:
class BuildingListCreateView(generics.ListCreateAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    # permission_classes = [permissions.IsAuthenticated]

class BuildingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    # permission_classes = [permissions.IsAuthenticated]

class GetKanbanData(APIView):
    def get(self, request):
        if request.user.role == "user" and not request.user.is_superuser:
            return Response({"response":"Unauthorized"})
        company = Company.objects.filter(
            owner=request.user
        ).first()
        users = User.objects.filter(role="tech", company=company)
        maintenance_columns = KanbanColumn.objects.filter(company=company).order_by('order')
        serializer = FullKanbanColumnSerializer(maintenance_columns, many=True, context={"request":request})
        context =  {"columns": serializer.data, "users": users}
        return Response(context)
    
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def list(self, request):
        # Get notifications for the authenticated user
        user = request.user
        notifications = Notification.objects.filter(Q(recipient=user)|Q(event='change'))

        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def latest(self, request):
        # Get notifications for the authenticated user
        user = request.user
        notifications = Notification.objects.filter(Q(recipient=user)|Q(event='change'), is_seen=False)

        # Mark notifications as seen
        for notification in notifications:
            notification.is_seen = True
            notification.save()

        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
