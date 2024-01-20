from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from expenses.models import Expense  # Assuming 'expenses' is the app name

class Expense2(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=266)
    expense = models.ForeignKey(to=Expense, on_delete=models.CASCADE, related_name='linked_expense')

    def __str__(self):
        return self.category

    class Meta:
        ordering = ['-date']
