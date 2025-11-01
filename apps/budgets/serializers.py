from rest_framework import serializers
from .models import Budget
from django.db.models import Sum
from apps.transactions.models import Transaction
from datetime import datetime

class BudgetSerializer(serializers.ModelSerializer):
    """
    Budget serializer with additional computed fields.
    """
    actual_expenses = serializers.SerializerMethodField()
    remaining = serializers.SerializerMethodField()
    percentage_used = serializers.SerializerMethodField()
    
    class Meta:
        model = Budget
        fields = [
            'id', 'month', 'budget_amount', 
            'actual_expenses', 'remaining', 'percentage_used',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_actual_expenses(self, obj):
        """
        Calculate actual expenses for the budget month.
        """
        # Get start and end of month
        year = obj.month.year
        month = obj.month.month
        
        # Get next month for end date
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year
        
        start_date = datetime(year, month, 1).date()
        end_date = datetime(next_year, next_month, 1).date()
        
        # Sum expenses for the month
        expenses = Transaction.objects.filter(
            user=obj.user,
            type='expense',
            date__gte=start_date,
            date__lt=end_date
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        return str(expenses)
    
    def get_remaining(self, obj):
        """
        Calculate remaining budget.
        """
        actual = float(self.get_actual_expenses(obj))
        budget = float(obj.budget_amount)
        remaining = budget - actual
        return str(remaining)
    
    def get_percentage_used(self, obj):
        """
        Calculate percentage of budget used.
        """
        actual = float(self.get_actual_expenses(obj))
        budget = float(obj.budget_amount)
        
        if budget == 0:
            return 0
        
        percentage = (actual / budget) * 100
        return round(percentage, 2)