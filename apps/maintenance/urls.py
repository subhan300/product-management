from django.urls import path
from apps.maintenance.api.views import GetKanbanData, AssignEmployeeView, CreateMessageView, KanbanView, MessageView, MoveNextView, MovePreviousView, MoveToView, NotificationViewSet
from apps.maintenance.views import (
    DeleteMaintenanceView,
    MaintenanceView,
    DashboardView,
    GetUnits,
    GetRooms,
    GetIssues,
    GetMaintenanceItems,
    GetMaintenanceDetails,   
)


urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("maintenance/", MaintenanceView.as_view(), name="maintenance"),
    
    
    path(
        "api/maintenance_delete/",
        DeleteMaintenanceView.as_view(),
        name="maintenance-delete",
    ),
    path(
        "api/maintenance_detail/<int:pk>/",
        GetMaintenanceDetails.as_view(),
        name="maintenance-detail",
    ),
    path("api/kanban/", KanbanView.as_view(), name="kanban"),
    path("api/messages/", CreateMessageView.as_view(), name="create-messages"),
    path("api/assignuser/", AssignEmployeeView.as_view(), name="assignuser"),
    path("api/movenext/", MoveNextView.as_view(), name="movenext"),
    path("api/moveprevious/", MovePreviousView.as_view(), name="moveprevious"),
    path("api/moveto/", MoveToView.as_view(), name="moveto"),
    path("api/messages/<int:pk>", MessageView.as_view(), name="messages"),
    path("api/getunits/<str:building_name>",GetUnits.as_view(), name="units"),
    path("api/getrooms/<str:unit_name>",GetRooms.as_view(), name="rooms"),
    path("api/getissues/<str:m_item>",GetIssues.as_view(), name="maintenance_issues"),
    path("api/get_m_items/<str:room_no>",GetMaintenanceItems.as_view(), name="maintenanace_items"),
    path("api/getkanbandata/",GetKanbanData.as_view(), name="kanban_data"),
    path("api/deletemaintenance/",DeleteMaintenanceView.as_view(), name="delete_maintenance"),
    path("api/notifications/",NotificationViewSet.as_view({'get': 'list'}), name="notifications"),
    path("api/notifications/latest",NotificationViewSet.as_view({'get': 'latest'}), name="latest_notifications"),
]
