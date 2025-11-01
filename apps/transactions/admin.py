from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['description', 'type', 'amount', 'category', 'user', 'date']
    list_filter = ['type', 'date', 'created_at']
    search_fields = ['description', 'user__username']
    date_hierarchy = 'date'