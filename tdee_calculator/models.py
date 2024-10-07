from django.db import models

class UserData(models.Model):
    weight = models.FloatField()
    height = models.FloatField()
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    activity_level = models.FloatField()
    goal = models.CharField(max_length=10, choices=[('lose', 'Lose Weight'), ('maintain', 'Maintain Weight'), ('gain', 'Gain Weight')])

class Meal(models.Model):
    MEAL_TYPES = [
        ('vegetable', 'Vegetable'),
        ('snack', 'Snack'),
        ('main', 'Main Meal'),
        ('red_meat', 'Red Meat'),
        ('white_meat', 'White Meat'),
        ('fish', 'Fish'),
        ('grain', 'Grain'),
        ('dairy', 'Dairy'),
        ('fruit', 'Fruit'),
        ('dessert', 'Dessert'),
        ('beverage', 'Beverage'),
    ]

    name = models.CharField(max_length=100)
    calories = models.FloatField()
    protein = models.FloatField(help_text="Protein in grams")
    carbs = models.FloatField(help_text="Carbohydrates in grams")
    fats = models.FloatField(help_text="Fats in grams")
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    image = models.ImageField(upload_to='meal_images/', null=True, blank=True)
    
    # New fields for better nutritional tracking
    fiber = models.FloatField(default=0, help_text="Fiber in grams")
    sugar = models.FloatField(default=0, help_text="Sugar in grams")
    sodium = models.FloatField(default=0, help_text="Sodium in milligrams")
    vitamins = models.TextField(blank=True, help_text="List of vitamins present")
    minerals = models.TextField(blank=True, help_text="List of minerals present")

    def __str__(self):
        return f"{self.name} - {self.calories} kcal"