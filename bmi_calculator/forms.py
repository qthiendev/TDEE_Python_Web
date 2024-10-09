from django import forms

class BMIForm(forms.Form):
    height = forms.FloatField(label='Chiều cao (cm)', min_value=1)
    weight = forms.FloatField(label='Cân nặng (kg)', min_value=1)
