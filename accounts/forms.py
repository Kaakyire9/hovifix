from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'employee_number',
            'email',
            'department',
            'shift',
            'password1',
            'password2',
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'Staff'  # default role
        if commit:
            user.save()
        return user
