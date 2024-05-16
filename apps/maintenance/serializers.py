from rest_framework import serializers
from apps.accounts.serializers import ShortUserSerializer
from apps.maintenance.models import Image, KanbanColumn, MaintenanceRequest, MaintenanceAssigning,MaintenanceDetail, Message
from django.utils import timezone
from django.template.defaultfilters import date
from django.utils.timesince import timesince
from django.db.models import Q
from rest_framework import serializers
from apps.maintenance.models import (
    Company, 
    Building, 
    Notification, 
    Unit, 
    Room, 
    MaintenanceItem, 
    Issue, 
    IssueDetails, 
    KanbanColumn, 
    Image,
    MaintenanceRequest, 
    Message, 
    MaintenanceAssigning
)


class ShortKanbanColumnSerializer(serializers.ModelSerializer):

    class Meta:
        model = KanbanColumn
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'


class CreateMessageSerializer(serializers.ModelSerializer):
    attachment = serializers.FileField(required=False)
    class Meta:
        model = Message
        fields = ["user", "message", "maintenance","attachment"]


class ShortKanbanSerializer(serializers.ModelSerializer):
    class Meta:
        model = KanbanColumn
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer()
    created_at_ago = serializers.SerializerMethodField()
    
    def get_created_at_ago(self, obj):
        # Calculate the time difference between obj.created_at and now
        return timesince(obj.created_at, timezone.now())
    

    class Meta:
        model = Message
        fields = ["user", "message", "created_at", "created_at_ago", "attachment"]
        
        
class AssingedEmployeeSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer()
    class Meta:
        model = MaintenanceAssigning
        fields = ["id", "user"]


class MaintenanceSerializer(serializers.ModelSerializer):
    status = ShortKanbanColumnSerializer()
    user = ShortUserSerializer()
    messages = serializers.SerializerMethodField()
    assined_user = serializers.SerializerMethodField()
    issues = serializers.SerializerMethodField()
    problemImages = ImageSerializer(many=True)
    next_status = serializers.SerializerMethodField()
    previous_status = serializers.SerializerMethodField()
    next_status = serializers.SerializerMethodField()
    previous_status = serializers.SerializerMethodField()
    
    created_at_ago = serializers.SerializerMethodField()
    
    def get_created_at_ago(self, obj):
        # Calculate the time difference between obj.created_at and now
        return timesince(obj.enquiryDate, timezone.now())
    

    def get_next_status(self, obj):
        column = KanbanColumn.objects.filter(order=obj.status.order+1).first()
        if column:
            return ShortKanbanSerializer(column).data
        return None
    
    def get_previous_status(self, obj):
        column = KanbanColumn.objects.filter(order=obj.status.order-1).first()
        if column:
            return ShortKanbanSerializer(column).data
        return None
        

    def get_issues(self, obj):
        return MaintenanceDetailSerializer(obj.maintenance_detail.all(), many=True).data

    def get_assined_user(self, obj):
        return AssingedEmployeeSerializer(obj.maintenance_assigning.all(), many=True).data

    def get_messages(self, obj):
        messages = Message.objects.filter(maintenance=obj).order_by("-created_at")
        return MessageSerializer(messages.all(), many=True).data    


    class Meta:
        model = MaintenanceRequest
        fields = '__all__'


class MaintenanceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceDetail
        fields = '__all__'

        
class MaintenanceStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRequest
        fields = ['status']  # Specify the fields you want to allow for updating

    def validate_status(self, value):
        columns = KanbanColumn.objects.all().values_list('status', flat=True)
        if value not in [column.name for column in columns]:
            raise serializers.ValidationError("Invalid status")
        return value




class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class MaintenanceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceItem
        fields = '__all__'

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'

class IssueDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueDetails
        fields = '__all__'

class KanbanColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = KanbanColumn
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class MaintenanceRequestSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer()
    status = ShortKanbanSerializer()
    room = RoomSerializer()
    maintenance_item = MaintenanceItemSerializer()
    building = BuildingSerializer()
    unit = UnitSerializer()
    issue = IssueSerializer()
    assigned_users = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()
    problemImage = ImageSerializer(many=True)
    created_at_ago = serializers.SerializerMethodField()
    formatted_enquiry_date = serializers.SerializerMethodField()
    
    next_status = serializers.SerializerMethodField()
    previous_status = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def get_description(self, obj):
        description = f'''
                <p style="text-align:justify;">
                {obj.user.first_name} submitted an issue {self.get_created_at_ago(obj)} ago. They have encountered a maintenance problem in {obj.building.name}, which is located in the {obj.unit.name} unit. The issue is specifically in room {obj.room.room_no} and is related to the maintenance item called <b>{obj.maintenance_item.name}</b>.<br/>
                    The issue description provided by the user is as follows: <b>{obj.issue_details}</b>.

                    The status of this maintenance request is currently <b>{obj.status.name},</b> and it has been assigned the color code <b>{obj.status.color_class}</b> to indicate its urgency.

                    Please take the necessary steps to address this issue promptly and ensure a resolution in a timely manner. If you have any questions or need further information, please reach out to the user or the assigned personnel.
                    </p>
'''
        return description

    

    def get_next_status(self, obj):
        
        request = self.context.get('request')
        column = KanbanColumn.objects.filter(order=obj.status.order+1, company=request.user.company).first()
        if column:
            return ShortKanbanSerializer(column).data
        return None
    
    def get_previous_status(self, obj):
        request = self.context.get('request')
        column = KanbanColumn.objects.filter(order=obj.status.order-1, company=request.user.company).first()
        if column:
            return ShortKanbanSerializer(column).data
        return None
        

    def get_created_at_ago(self, obj):
        # Calculate the time difference between obj.created_at and now
        return timesince(obj.enquiryDate, timezone.now())
    def get_formatted_enquiry_date(self, obj):
        return date(obj.enquiryDate, "Y-m-d") 

    def get_problemImages(self,obj):
        return ImageSerializer(Image.objects.filter(maintenance=obj), many=True).data

    def get_messages(self,obj):
        return MessageSerializer(Message.objects.filter(maintenance=obj).order_by("-created_at"), many=True).data
    
    def get_assigned_users(self,obj):
        return MaintenanceAssigningSerializer(MaintenanceAssigning.objects.filter(maintenance=obj), many=True).data

    class Meta:
        model = MaintenanceRequest
        fields = '__all__'

class MaintenanceAssigningSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer()
    
    class Meta:
        model = MaintenanceAssigning
        fields = '__all__'

class FullKanbanColumnSerializer(serializers.ModelSerializer):
    maintenances = serializers.SerializerMethodField()
    def get_maintenances(self, obj):
        request = self.context.get('request')
        assigned_maintenance_ids = MaintenanceAssigning.objects.filter(
            user=request.user
        ).values_list('maintenance_id', flat=True)
        maintenances = MaintenanceRequest.objects.filter(company=request.user.company, status=obj, is_deleted=False)
        # if request.user.role!='manager' and request.user.role!='tech':
        #     maintenances = maintenances.filter(
        #         Q(unit=request.user.primary_unit) | 
        #         Q(unit__temporary_assigned_resource=request.user)
        #   )
        
        three_days_ago = timezone.now() - timezone.timedelta(days=3)

        maintenances = maintenances.exclude(
            status__status_code="cp",
            # updated_at__lte=three_days_ago
        )
        return MaintenanceRequestSerializer(maintenances.all(), many=True, context={"request": request}).data

    class Meta:
        model = KanbanColumn
        fields = '__all__'