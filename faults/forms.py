from django import forms
from accounts.models import CustomUser
from faults.models import FaultCall

class AssignEngineerForm(forms.ModelForm):
    class Meta:
        model = FaultCall
        fields = ['assigned_engineer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter staff in the Engineering department
        self.fields['assigned_engineer'].queryset = CustomUser.objects.filter(
            role='Staff', department='Engineering'
        )
