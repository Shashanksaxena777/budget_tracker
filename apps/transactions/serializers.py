from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'category', 'category_name', 'type', 'amount', 'description', 'date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']