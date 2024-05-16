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
from .models import InventoryType, Inventory


class DashboardInventoryView(LoginRequiredMixin, View):
    template_name = 'inventory/dashboard.html'
    def get(self, request):
        user = request.user
        company = user.company
    
        inventroy_types = InventoryType.objects.all()
        inventories = Inventory.objects.all()
        context =  {
            "inventroy_types": inventroy_types,
            "inventories": inventories,
            
        }
        cards = [{'label':"All Inventory", 'value':inventories.count()}]
        for inventory in inventroy_types:
            context[f'{inventory.name}'] = inventories.filter(type__name=inventory.name).count()
            cards.append({'label':f'{inventory.name}','value':context[f'{inventory.name}'], 'icon':f'{inventory.icon.image if inventory.icon else None}'})
        context['cards'] = cards
        print(cards)
        response = render(request, self.template_name, context)
        response.context_data = context
        return response

