from django.db import models
from django.contrib.auth.models import User

class Budget(models.Model):
    """
    Monthly budget model.
    
    Each user can have one budget per month.
    Stores the budget amount and the month it applies to.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    month = models.DateField(help_text="First day of the month")
    budget_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        # One budget per user per month
        unique_together = ['user', 'month']
        ordering = ['-month']
    
    def __str__(self):
        return f"{self.user.username} - {self.month.strftime('%B %Y')} - ₹{self.budget_amount}"