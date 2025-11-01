from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        unique_together = ['user', 'name', 'type']
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.type})"