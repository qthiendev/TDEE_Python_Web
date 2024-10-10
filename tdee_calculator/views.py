from django.shortcuts import render
import random
from .forms import TDEEForm
from .models import Meal

def calculate_bmr(weight, height, age, gender):
    """Calculate BMR using the Mifflin-St Jeor Equation."""
    if gender == 'Male':
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

def calculate_tdee(request):
    if request.method == 'POST':
        form = TDEEForm(request.POST)
        if form.is_valid():
            # Extract data
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            activity_level = float(form.cleaned_data['activity_level'])
            goal = form.cleaned_data['goal']

            # Calculate BMR and TDEE
            bmr = calculate_bmr(weight, height, age, gender)
            tdee = bmr * activity_level

            # Adjust TDEE based on goal
            if goal == 'lose':
                tdee -= 500         
            elif goal == 'gain':
                tdee += 500

            # Define recommended daily intake for food types (grams)
            recommended_intake = { 'vegetable': 300, 'snack': 50, 'main': 500, 'red_meat': 200, 'white_meat': 200, 'fish': 200,'grain': 250,'dairy': 200,'fruit': 200,'dessert': 100,'beverage': 200}

            # Define nutritional values per 100g for each meal type
            nutritional_values = {
                'vegetable': {'protein': 2, 'carbs': 5, 'fats': 0.5},
                'snack': {'protein': 5, 'carbs': 20, 'fats': 10},
                'main': {'protein': 20, 'carbs': 30, 'fats': 10},  # example for main meals
                'red_meat': {'protein': 25, 'carbs': 0, 'fats': 15},
                'white_meat': {'protein': 25, 'carbs': 0, 'fats': 10},
                'fish': {'protein': 22, 'carbs': 0, 'fats': 5},
                'grain': {'protein': 10, 'carbs': 75, 'fats': 1},
                'dairy': {'protein': 8, 'carbs': 5, 'fats': 10},
                'fruit': {'protein': 1, 'carbs': 15, 'fats': 0.3},
                'dessert': {'protein': 2, 'carbs': 40, 'fats': 5},
                'beverage': {'protein': 0, 'carbs': 5, 'fats': 0}   # typically low in protein
            }

            # Calculate daily nutritional goals based on recommendations
            daily_protein = sum((recommended_intake[item] / 100) * nutritional_values[item]['protein'] for item in recommended_intake)
            daily_carbs = sum((recommended_intake[item] / 100) * nutritional_values[item]['carbs'] for item in recommended_intake)
            daily_fats = sum((recommended_intake[item] / 100) * nutritional_values[item]['fats'] for item in recommended_intake)

            # Fetch meals and filter
            meals = Meal.objects.filter(calories__lte=tdee)
            balanced_meals = filter_balanced_meals(meals, daily_protein, daily_carbs, daily_fats, tdee)

            # Check if balanced_meals is empty
            if not balanced_meals:
                balanced_meals = meals  # Fallback to all meals if no balanced meals are found

            return render(request, 'results.html', {'tdee': tdee, 'meals': balanced_meals})
    else:
        form = TDEEForm()

    return render(request, 'tdee.html', {'form': form})

def filter_balanced_meals(meals, daily_protein, daily_carbs, daily_fats, tdee):
    """Filter meals to ensure they meet daily nutritional balance criteria and stay within calorie limits."""
    balanced_meals = []

    # Initialize total intake trackers
    total_protein = 0
    total_carbs = 0
    total_fats = 0
    total_calories = 0

    shuffled_meals = list(meals)  # Convert QuerySet to a list
    random.shuffle(shuffled_meals)  # Shuffle the list

    for meal in shuffled_meals:
        # Extract nutritional values
        protein = meal.protein
        carbs = meal.carbs
        fats = meal.fats
        calories = meal.calories

        # Check if adding this meal would exceed daily nutritional goals and total calories
        if (total_protein + protein <= daily_protein and
            total_carbs + carbs <= daily_carbs and
            total_fats + fats <= daily_fats and
            total_calories + calories <= tdee):  # Check against tdee
            # Add meal to balanced meals
            balanced_meals.append(meal)

            # Update total intake
            total_protein += protein
            total_carbs += carbs
            total_fats += fats
            total_calories += calories

            # Print meal details for debugging
            print(f"Added: {meal.name} - Total Calories: {total_calories}, Protein: {total_protein}g, Carbs: {total_carbs}g, Fats: {total_fats}g")

        # Break if we've met or exceeded all daily goals
        if (total_protein >= daily_protein and
            total_carbs >= daily_carbs and
            total_fats >= daily_fats and
            total_calories <= tdee):  # Ensure total calories is also checked
            break

    return balanced_meals