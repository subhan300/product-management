from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views import View
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from apps.maintenance.models import *
from apps.maintenance.serializers import FullKanbanColumnSerializer, IssueSerializer, \
    MaintenanceItemSerializer, MaintenanceRequestSerializer, RoomSerializer, UnitSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.maintenance.serializers import  FullKanbanColumnSerializer
from django.utils import timezone

User = get_user_model()

class DashboardView(LoginRequiredMixin, View):
    template_name = 'maintenance/dashboard.html'
    def get(self, request):
        user = request.user
        company = user.company
    
        # three_days_ago = timezone.now() - timezone.timedelta(days=3)
        maintenances = MaintenanceRequest.objects.filter(
            Q(company=company) &
            Q(is_deleted=False)
        ).order_by('-id')
        assigned_to_me = 0
        
        assigned_requests = MaintenanceAssigning.objects.filter(maintenance__company=company)
        # if user.role != "manager" and user.role != "tech":
            # maintenances = maintenances.filter(
            #     Q(unit__temporary_assigned_resource=user)
            # ).distinct()
            #  Q(unit=user.primary_unit) |
            # assigned_requests = assigned_requests.filter(maintenance__unit=request.user.primary_unit)
            

        assigned_to_me = MaintenanceAssigning.objects.filter(user=user).count()
        n_maintenance_items = maintenances.count()
        n_assigned_requests = MaintenanceRequest.objects.filter(Q(id__in=assigned_requests.values_list('maintenance_id')) & Q(is_deleted=False))
        audit_maintenance_requests = maintenances.filter(request_type='audit', company=request.user.company).count()
        un_assigned_requests = n_maintenance_items - n_assigned_requests.count()
        columns = KanbanColumn.objects.all().order_by('order')
        building = Building.objects.filter(company=company)
        maintenance_items = MaintenanceItem.objects.filter(company=company)
        
        if user.is_superuser:
            n_maintenance_items = MaintenanceRequest.objects.all().count()
            assigned_requests = MaintenanceAssigning.objects.all().values_list('maintenance_id')
            n_assigned_requests = MaintenanceRequest.objects.filter(Q(id__in=assigned_requests) & Q(is_deleted=False))
            un_assigned_requests = MaintenanceRequest.objects.filter(~Q(id__in=assigned_requests) & Q(is_deleted=False)).count()
        context =  {
            "columns": columns,
            "n_maintenance_items": n_maintenance_items,
            "audit_maintenance_requests":audit_maintenance_requests,
            "n_assigned_requests":n_assigned_requests.count(),
            "un_assigned_requests":un_assigned_requests,
            "assigned_to_me":assigned_to_me,
            "maintenances": maintenances,
            "buildings":building,
            "maintenance_items":maintenance_items,
            "company":request.user.company,
            "notifications": Notification.objects.filter(Q(event='new_assignment')|Q(event='new_message'), recipient=request.user).order_by('-timestamp')[:6],
            "any_notifications": Notification.objects.filter(Q(event='new_assignment')|Q(event='new_message'), is_seen=False).order_by('-timestamp').count()>0,
            
        }
        cards = [{'label':"All Requests", 'value':maintenances.count()}]
        for column in columns:
            context[f'{column.name}'] = maintenances.filter(status__name=column.name).count()
            cards.append({'label':f'{column.name}','value':context[f'{column.name}'], 'icon':f'{column.icon.image if column.icon else None}'})
        context['cards'] = cards
        response = render(request, self.template_name, context)
        response.context_data = context
        return response

class MaintenanceView(LoginRequiredMixin, View):
    template_name = 'maintenance/system.html'

    def get(self, request):
        maintenance_columns = KanbanColumn.objects.all().order_by('order')
        users = User.objects.all()

        if not request.user.is_superuser:
            maintenance_columns = KanbanColumn.objects.filter(company=request.user.company).order_by('order')
            users = users.filter(company=request.user.company)

        serializer = FullKanbanColumnSerializer(maintenance_columns, many=True, context={"request":request})
        role = request.user.role
        context =  {"columns": serializer.data, "users": users, 'role':role}
        response = render(request, self.template_name, context)
        response.context_data = context
        return response

    def post(self, request):
        request_title = request.POST.get('request_title')
        maintenance_id = request.POST.get('maintenance_id')
        request_type = request.POST.get('request_type')
        end_date = request.POST.get('end_date')
        issue_building = request.POST.get('issue_building')
        issue_unit = request.POST.get('issue_unit')
        issue_room = request.POST.get('issue_room')
        issue_mantenance_item = request.POST.get('issue_maintenance_item')
        item_issue = request.POST.get('item_issue')
        issue_date =request.POST.get('request_date')
        other_m_item_issue = request.POST.get('other_m_item_issue',None)
        maintenance_issue_description = request.POST.get('maintenance_issue_description')
        images = request.FILES.getlist('images')

        
        
        if other_m_item_issue:
            Issue.objects.create(
                title=other_m_item_issue,
                maintenance_item=MaintenanceItem.objects.filter(name=issue_mantenance_item).first(),
            )
            item_issue = other_m_item_issue
            
        if maintenance_id == "":
            maintenance = MaintenanceRequest.objects.create(
                request_title=request_title, 
                user=request.user, 
                enquiryDate=issue_date,
                request_type=request_type,
                end_date=end_date if end_date else None,
                building=Building.objects.filter(name=issue_building).first(),
                unit=Unit.objects.filter(name=issue_unit).first(),
                room=Room.objects.filter(room_no=issue_room).first(),
                maintenance_item=MaintenanceItem.objects.filter(name=issue_mantenance_item).first(),
                issue=Issue.objects.filter(title=item_issue).first(),
                issue_details=maintenance_issue_description,               
                company=request.user.company,
                status=KanbanColumn.objects.filter(status_code="pending", company=request.user.company).first())
        else:
            maintenance = MaintenanceRequest.objects.filter(id=maintenance_id).first()
            maintenance.request_title = request_title
            maintenance.enquiryDate = issue_date
            maintenance.building = Building.objects.filter(name=issue_building).first()
            maintenance.room = Room.objects.filter(room_no=issue_room).first()
            maintenance.unit = Unit.objects.filter(name=issue_unit).first()
            maintenance.maintenance_item = MaintenanceItem.objects.filter(name=issue_mantenance_item).first()
            maintenance.issue = Issue.objects.filter(title=item_issue).first()
            maintenance.issue_details = maintenance_issue_description
            maintenance.save()
            
        # Add the new images
        for image_file in images:
            image = Image.objects.create(
                image=image_file,
                alt=request_title,
                company=request.user.company,
            )
            maintenance.problemImage.add(image)
        
        MaintenanceAssigning.objects.create(user=request.user, maintenance=maintenance)
        
        return redirect('dashboard')


class KanbanView(APIView):
    
    def get(self, request):
        if request.user.role=="user" and not request.user.is_superuser:
            return redirect('dashboard')
        maintenance_columns = KanbanColumn.objects.all().order_by('order')
        serializer = FullKanbanColumnSerializer(maintenance_columns, many=True, context={"request":request})
        return Response(serializer.data)


class DeleteMaintenanceView(View):
    def post(self, request):
        if "maintenance_delete_id" in request.POST:
            maintenance = MaintenanceRequest.objects.filter(id=request.POST["maintenance_delete_id"]).first()
            maintenance.is_deleted = True
            maintenance.save()
            return redirect("dashboard")
        return Response({"message": "maintenance_delete_id -> Field is required..."})


class DeleteMaintenanceView(View):
    def post(self, request):
        maintenance_id = request.POST.get("maintenance_delete_id")
        cancel_request_type = request.POST.get('cancel_reason')
        if maintenance_id:
            maintenance = get_object_or_404(MaintenanceRequest, id=maintenance_id)
            kanbancol = KanbanColumn.objects.filter(name="Cancelled").first()
            maintenance.cancel_reason = cancel_request_type
            maintenance.status = kanbancol
            maintenance.save()
        return redirect('dashboard')

class GetUnits(APIView):
    def get(self, request,building_name):
        units = Unit.objects.all()
        # units = Unit.objects.filter(
        #     Q(building__name=building_name),
        # )
        # if request.user.role!="manager":
        #     units = units.filter(
        #         Q(temporary_assigned_resource=request.user),
            # )
            
            # |Q(id=request.user.primary_unit.id)
        
        return Response({"units": UnitSerializer(units, many=True).data})

class GetRooms(APIView):
    def get(self, request, unit_name):
        rooms = Room.objects.filter(
            unit__name=unit_name
        ).order_by('room_no')
        
        return Response({"room": RoomSerializer(rooms, many=True).data})

class GetIssues(APIView):
    def get(self, request, m_item):
        maintenance_issues = Issue.objects.filter(
            maintenance_item__name=m_item
        )
        
        return Response({"issues": IssueSerializer(maintenance_issues, many=True).data})

class GetMaintenanceItems(APIView):
    
    def get(self, request, room_no):
        maintenance_items = MaintenanceItem.objects.filter(company=request.user.company).order_by('name')
        return Response({"maintenance_items": MaintenanceItemSerializer(maintenance_items, many=True).data})

class GetMaintenanceDetails(APIView):

    def get(self, request, pk):
        maintenance_request = MaintenanceRequest.objects.filter(
            id=pk
        ).first()
        units = Unit.objects.filter(building=maintenance_request.building)
        rooms = Room.objects.filter(unit=maintenance_request.unit)
        maintenance_items = MaintenanceItem.objects.filter(company=maintenance_request.company)
        
        issues = Issue.objects.filter(maintenance_item=maintenance_request.maintenance_item)
        maintenance_data = MaintenanceRequestSerializer(maintenance_request, context={"request":request}).data
        unit_data = UnitSerializer(units, many=True).data
        maintenance_item_data = MaintenanceItemSerializer(maintenance_items, many=True).data
        issues_data = IssueSerializer(issues, many=True).data
        kanban_columns = KanbanColumn.objects.filter(company=maintenance_request.company)
        # Convert the queryset into a list of dictionaries
        kanban_columns_list = [{'id': column.id, 'name': column.name, 'order': column.order} for column in kanban_columns]

        # Now, you can serialize kanban_columns_list into JSON
        import json
        kanban_columns_json = json.dumps(kanban_columns_list)

        room_data = RoomSerializer(rooms, many=True).data
        maintenance_data['maintenance_items'] = maintenance_item_data
        maintenance_data['issues'] = issues_data
        maintenance_data['rooms'] = room_data
        maintenance_data['units'] = unit_data
        maintenance_data['columns'] = kanban_columns_json

        return Response(maintenance_data, status=status.HTTP_200_OK)
        