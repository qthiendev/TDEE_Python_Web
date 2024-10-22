# Generated by Django 5.1.1 on 2024-10-07 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tdee_calculator', '0004_meal_meal_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='fiber',
            field=models.FloatField(default=0, help_text='Fiber in grams'),
        ),
        migrations.AddField(
            model_name='meal',
            name='minerals',
            field=models.TextField(blank=True, help_text='List of minerals present'),
        ),
        migrations.AddField(
            model_name='meal',
            name='sodium',
            field=models.FloatField(default=0, help_text='Sodium in milligrams'),
        ),
        migrations.AddField(
            model_name='meal',
            name='sugar',
            field=models.FloatField(default=0, help_text='Sugar in grams'),
        ),
        migrations.AddField(
            model_name='meal',
            name='vitamins',
            field=models.TextField(blank=True, help_text='List of vitamins present'),
        ),
        migrations.AlterField(
            model_name='meal',
            name='meal_type',
            field=models.CharField(choices=[('vegetable', 'Vegetable'), ('snack', 'Snack'), ('main', 'Main Meal'), ('red_meat', 'Red Meat'), ('white_meat', 'White Meat'), ('fish', 'Fish'), ('grain', 'Grain'), ('dairy', 'Dairy'), ('fruit', 'Fruit'), ('dessert', 'Dessert'), ('beverage', 'Beverage')], max_length=20),
        ),
    ]
