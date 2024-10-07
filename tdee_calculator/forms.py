from django import forms
from .models import UserData

class TDEEForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['weight', 'height', 'age', 'gender', 'activity_level', 'goal']
