from django.contrib import admin
from .models import Budget

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['user', 'month', 'budget_amount', 'created_at']
    list_filter = ['month', 'created_at']
    search_fields = ['user__username']
    date_hierarchy = 'month'