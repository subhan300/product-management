from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.models import LogEntry
from apps.accounts.models import Action, CustomUser
from django.utils.html import format_html
from apps.maintenance.admin import FormFieldBaseAdmin

from apps.maintenance.models import Company, Image, Unit

admin.site.site_title = 'Maintenance System'
admin.site.site_header = 'Maintenance System'
admin.site.index_title = 'Maintenance System'

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'company', 'primary_unit', 'phone', 'username', 'bio', 'profile_image')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', "last_activity")}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', "username", "first_name", "last_name", 'company', 'primary_unit', 'password1', 'password2', 'is_staff', "role"),
        }),
    )
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Limit the choices for foreign key fields to those associated with the current user's company
        if not request.user.is_superuser:
            if db_field.name == 'company':
                kwargs['queryset'] = Company.objects.filter(owner=request.user)
            if db_field.name == 'profile_image':
                kwargs['queryset'] = Image.objects.filter(company=request.user.company)
            if db_field.name == 'primary_unit':
                kwargs['queryset'] = Unit.objects.filter(building__company=request.user.company)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_queryset(self, request):
        # Limit the queryset based on user's role
        if not request.user.is_superuser:
            self.fieldsets = (
                (None, {'fields': ('email', 'password')}),
                ('Personal Info', {'fields': ('first_name', 'last_name', 'company', 'phone', 'username', 'bio', 'profile_image')}),
                ('Permissions', {'fields': ('role', 'is_active', 'is_staff',)}),
                ('Important dates', {'fields': ('last_login', 'date_joined', "last_activity")}),
            )
            return CustomUser.objects.filter(company=request.user.company)
        return CustomUser.objects.all()

class ActionAdmin(FormFieldBaseAdmin):
    def link_url(self, obj):
        return format_html('<a href="{}">{}</a>'.format(obj.url, obj.url))

    list_display = ('user', 'link_url', 'action_type', 'timestamp')
    list_filter = ('user', 'user__role', 'action_type', 'timestamp')
    search_fields = ('user__email', 'action_type')
    date_hierarchy = 'timestamp'

    
    def get_queryset(self, request):
        # Limit the queryset based on user's role
        if not request.user.is_superuser:
            return Action.objects.filter(user__company=request.user.company)
        return Action.objects.all()
    


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_id', 'action_flag', 'change_message')
    list_filter = ('action_time', 'user', 'content_type', 'action_flag')
    search_fields = ('user__username', 'content_type__model', 'object_id')
    date_hierarchy = 'action_time'

admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(Action, ActionAdmin)

admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(Image)
