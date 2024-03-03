# forms.py
from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['profile_pic','id','first_name', 'last_name', 'dept', 'salary', 'bonus', 'role', 'phone', 'hire_date']
        # Add or remove fields as needed
