from django.shortcuts import render
from .forms import TDEEForm
from .models import Meal

def calculate_tdee(request):
    if request.method == 'POST':
        form = TDEEForm(request.POST)
        if form.is_valid():
            # Extract data
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            activity_level = form.cleaned_data['activity_level']
            goal = form.cleaned_data['goal']

            # Calculate BMR and TDEE
            bmr = calculate_bmr(weight, height, age, gender)
            tdee = bmr * activity_level
            if goal == 'lose':
                tdee -= 500
            elif goal == 'gain':
                tdee += 500

            print(f"TDEE: {tdee}")

            # Fetch meals
            meals = Meal.objects.filter(calories__lte=tdee)
            print("Fetched meals:")
            for meal in meals:
                print(meal.name, meal.calories)

            # Filter balanced meals
            balanced_meals = filter_balanced_meals(meals)

            return render(request, 'results.html', {'tdee': tdee, 'meals': balanced_meals})

    else:
        form = TDEEForm()
    return render(request, 'tdee.html', {'form': form})

def calculate_bmr(weight, height, age, gender):
    """Calculate BMR using the Mifflin-St Jeor Equation."""
    if gender == 'Male':
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

def filter_balanced_meals(meals):
    """Filter meals to ensure they meet nutritional balance criteria."""
    balanced_meals = []
    for meal in meals:
        total_calories = meal.calories
        protein_calories = meal.protein * 4  # 4 calories per gram of protein
        carb_calories = meal.carbs * 4  # 4 calories per gram of carbs
        fat_calories = meal.fats * 9  # 9 calories per gram of fat

        if total_calories > 0:  # Avoid division by zero
            protein_ratio = protein_calories / total_calories
            carb_ratio = carb_calories / total_calories
            fat_ratio = fat_calories / total_calories

            print(f"{meal.name} - Total Calories: {total_calories}, Protein Ratio: {protein_ratio}, Carb Ratio: {carb_ratio}, Fat Ratio: {fat_ratio}")

            # Adjust criteria to accommodate low-protein foods
            if (
                carb_ratio >= 0.5 and
                (protein_ratio >= 0.1 or meal.meal_type in ['vegetable', 'fruit']) and  # Allow lower protein for veggies/fruits
                fat_ratio <= 0.3
            ):
                balanced_meals.append(meal)

    return balanced_meals

