from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Financial summary endpoint"""
        transactions = self.get_queryset()
        
        income = transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
        expenses = transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
        
        return Response({
            'total_income': str(income),
            'total_expenses': str(expenses),
            'balance': str(income - expenses),
            'income_count': transactions.filter(type='income').count(),
            'expense_count': transactions.filter(type='expense').count(),
        })