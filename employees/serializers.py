from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee model."""
    
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'department', 'role', 'date_joined']
        read_only_fields = ['id', 'date_joined']
    
    def validate_name(self, value):
        """Validate that name is not empty."""
        if not value or not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value.strip()
    
    def validate_email(self, value):
        """Validate email format and uniqueness."""
        if not value:
            raise serializers.ValidationError("Email is required.")
        
        # Check uniqueness (excluding current instance if updating)
        instance = self.instance
        if instance:
            if Employee.objects.filter(email=value).exclude(pk=instance.pk).exists():
                raise serializers.ValidationError("An employee with this email already exists.")
        else:
            if Employee.objects.filter(email=value).exists():
                raise serializers.ValidationError("An employee with this email already exists.")
        
        return value.lower().strip()
