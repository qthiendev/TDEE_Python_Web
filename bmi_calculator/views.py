from django.shortcuts import render
from .forms import BMIForm

def calculate_bmi(request):
    bmi = None
    category = ""
    if request.method == 'POST':
        form = BMIForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height'] / 100

            # Calculate BMI
            bmi = weight / (height ** 2)
            bmi = round(bmi, 1)

            # Determine BMI category
            if bmi < 16: category = "Severe Thinness"
            elif 16 <= bmi < 17: category = "Moderate Thinness"
            elif 17 <= bmi < 18.5: category = "Mild Thinness"
            elif 18.5 <= bmi < 24.9: category = "Normal Weight"
            elif 25 <= bmi < 29.9: category = "Overweight"
            elif 30 <= bmi < 34.9: category = "Obesity Class I"
            elif 35 <= bmi < 39.9: category = "Obesity Class II"
            else: category = "Obesity Class III"

    else:
        form = BMIForm()

    return render(request, 'bmi.html', {'form': form, 'bmi': bmi, 'category': category})
