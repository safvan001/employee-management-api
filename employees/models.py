from django.db import models
from django.core.validators import EmailValidator
from django.utils import timezone


class Employee(models.Model):
    """Employee model for company employee management."""
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(
        max_length=255, 
        unique=True, 
        validators=[EmailValidator()],
        blank=False
    )
    department = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_joined']
        db_table = 'employees'
    
    def __str__(self):
        return f"{self.name} ({self.email})"
