from django.contrib import admin
from .models import Client, Document
from axes.models import AccessAttempt, AccessLog

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'client_type')
    search_fields = ('name',)

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'client', 'expiry_date', 'exists')
    list_filter = ('category', 'exists')
    search_fields = ('name', 'client__name')
