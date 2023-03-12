from django.contrib import admin
from .models import Paiements,OrderItem


class PaymAdmin(admin.ModelAdmin):
    list_display = [
        'idd',
        'numero',
        'ordered',
        'adresse',
        
    ]

admin.site.register(Paiements,PaymAdmin)
admin.site.register(OrderItem)