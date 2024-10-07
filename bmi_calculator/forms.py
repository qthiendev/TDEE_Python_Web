from django import forms

class BMIForm(forms.Form):
    weight = forms.FloatField(label='Weight (kg)', min_value=1)
    height = forms.FloatField(label='Height (cm)', min_value=1)
