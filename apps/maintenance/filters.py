from django.contrib import admin
from apps.maintenance.models import Room


class RoomUnitFilter(admin.SimpleListFilter):
    title = 'Unit'  # Displayed in the right sidebar
    parameter_name = 'unit'  # URL parameter

    def lookups(self, request, model_admin):
        # Get a list of all unique units
        units = Room.objects.values_list('unit__name', flat=True).distinct()
        return [(unit, unit) for unit in units]

    def queryset(self, request, queryset):
        if self.value():
            # Filter rooms by the selected unit
            return queryset.filter(unit__name=self.value())
        return queryset