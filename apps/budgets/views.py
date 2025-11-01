from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from datetime import datetime
from .models import Budget
from .serializers import BudgetSerializer
from apps.transactions.models import Transaction

class BudgetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Budget CRUD operations.
    """
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None  # No pagination for budgets
    
    def get_queryset(self):
        """
        Only return budgets for the current user.
        """
        return Budget.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """
        Set user when creating budget.
        """
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """
        Get current month's budget.
        
        Endpoint: GET /api/budgets/current/
        """
        # Get first day of current month
        today = datetime.now().date()
        current_month = datetime(today.year, today.month, 1).date()
        
        try:
            budget = Budget.objects.get(user=request.user, month=current_month)
            serializer = self.get_serializer(budget)
            return Response(serializer.data)
        except Budget.DoesNotExist:
            return Response(
                {'detail': 'No budget set for current month'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def comparison(self, request):
        """
        Get budget vs actual comparison for current month.
        
        Endpoint: GET /api/budgets/comparison/
        
        Returns:
        {
            "budget_amount": "50000.00",
            "actual_expenses": "28000.00",
            "remaining": "22000.00",
            "percentage_used": 56.0,
            "by_category": [...]
        }
        """
        # Get first day of current month
        today = datetime.now().date()
        current_month = datetime(today.year, today.month, 1).date()
        
        try:
            budget = Budget.objects.get(user=request.user, month=current_month)
        except Budget.DoesNotExist:
            return Response(
                {'detail': 'No budget set for current month'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Calculate expenses by category
        year = current_month.year
        month = current_month.month
        
        # Get next month for end date
        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year
        
        start_date = datetime(year, month, 1).date()
        end_date = datetime(next_year, next_month, 1).date()
        
        # Group expenses by category
        expenses_by_category = Transaction.objects.filter(
            user=request.user,
            type='expense',
            date__gte=start_date,
            date__lt=end_date
        ).values(
            'category__name', 'category__id'
        ).annotate(
            total=Sum('amount')
        ).order_by('-total')
        
        # Calculate totals
        total_expenses = sum(float(item['total']) for item in expenses_by_category)
        budget_amount = float(budget.budget_amount)
        remaining = budget_amount - total_expenses
        percentage_used = (total_expenses / budget_amount * 100) if budget_amount > 0 else 0
        
        return Response({
            'budget_amount': str(budget.budget_amount),
            'actual_expenses': str(total_expenses),
            'remaining': str(remaining),
            'percentage_used': round(percentage_used, 2),
            'by_category': [
                {
                    'category_id': item['category__id'],
                    'category_name': item['category__name'] or 'Uncategorized',
                    'amount': str(item['total']),
                    'percentage': round(float(item['total']) / total_expenses * 100, 2) if total_expenses > 0 else 0
                }
                for item in expenses_by_category
            ]
        })