from django.contrib import admin
from apps.accounts.models import CustomUser

from apps.maintenance.filters import RoomUnitFilter
from .models import (
    Company,
    Building,
    Image,
    MaintenanceAssigning,
    Message,
    Unit,
    Room,
    MaintenanceRequest,
    MaintenanceItem,
    Issue,
    KanbanColumn,
    MaintenanceDetail,
    MaintenanceAssigning,
)



class MaintenanceDetailInline(admin.TabularInline):
    model = MaintenanceDetail

class MaintenanceAssigningInline(admin.TabularInline):
    model = MaintenanceAssigning

class MessageInline(admin.TabularInline):
    model = Message

class UnitInline(admin.TabularInline):
    model = Unit

class BuildingInline(admin.TabularInline):
    model = Building

class RoomInline(admin.TabularInline):
    model = Room

class FormFieldBaseAdmin(admin.ModelAdmin):
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'problemImage':
                kwargs['queryset'] = Image.objects.filter(company=request.user.company)
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Limit the choices for foreign key fields to those associated with the current user's company
        if not request.user.is_superuser:
            if db_field.name == 'company':
                kwargs['queryset'] = Company.objects.filter(owner=request.user)
            if db_field.name == 'owner':
                kwargs['queryset'] = CustomUser.objects.filter(company=request.user.company)
            if db_field.name == 'user' or db_field.name == 'temporary_assigned_resource':
                kwargs['queryset'] = CustomUser.objects.filter(company=request.user.company)
            if db_field.name == 'maintenance_item':
                kwargs['queryset'] = MaintenanceItem.objects.filter(company=request.user.company)
            if db_field.name == 'maintenance':
                kwargs['queryset'] = MaintenanceRequest.objects.filter(company=request.user.company)
            if db_field.name == 'building':
                kwargs['queryset'] = Building.objects.filter(company=request.user.company)
            if db_field.name == 'unit':
                kwargs['queryset'] = Unit.objects.filter(building__company=request.user.company)
            if db_field.name == 'room':
                kwargs['queryset'] = Room.objects.filter(unit__building__company=request.user.company)
            if db_field.name == 'issue':
                kwargs['queryset'] = Issue.objects.filter(maintenance_item__company=request.user.company)
            if db_field.name == 'status':
                kwargs['queryset'] = KanbanColumn.objects.filter(company=request.user.company)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Company)
class CompanyAdmin(FormFieldBaseAdmin):
    list_display = ('name', 'address', 'phone', 'email', 'active', 'owner')
    inlines = [BuildingInline]
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(owner=request.user)
        return qs

@admin.register(Building)
class BuildingAdmin(FormFieldBaseAdmin):
    list_display = ('name', 'company')
    inlines = [UnitInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(company__owner=request.user)
        return qs

@admin.register(Unit)
class UnitAdmin(FormFieldBaseAdmin):
    list_display = ('name', 'building')
    inlines = [RoomInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(building__company__owner=request.user)
        return qs

@admin.register(Room)
class RoomAdmin(FormFieldBaseAdmin):
    list_display = ('room_no', 'unit')
    
    list_filter = (RoomUnitFilter,)

    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(unit__building__company__owner=request.user)
        return qs

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(FormFieldBaseAdmin):
    list_display = ('enquiryDate', 'request_title', 'user', 'building', 'unit', 'room', 'maintenance_item', 'status', 'updated_at')
    list_filter = ('status',)
    inlines = [MaintenanceDetailInline, MaintenanceAssigningInline, MessageInline]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(company__owner=request.user)
        return qs

@admin.register(MaintenanceItem)
class MaintenanceItemAdmin(FormFieldBaseAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(company=request.user.company)
        return qs

@admin.register(Issue)
class IssueAdmin(FormFieldBaseAdmin):
    list_display = ('title', 'maintenance_item')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(maintenance_item__company=request.user.company)
        return qs

@admin.register(KanbanColumn)
class KanbanColumnAdmin(FormFieldBaseAdmin):
    list_display = ('name', 'status_code', 'order', 'color_class', 'company')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(company__owner=request.user)
        return qs
    
@admin.register(MaintenanceAssigning)
class MaintenanceAssigningAdmin(FormFieldBaseAdmin):
    list_display = ('maintenance', 'user', 'created_at',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(user__company=request.user.company)
        return qs
    
admin.site.register(Image)
    