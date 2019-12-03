from django import forms
from Users.models import Profile
from . models import Dietplan, Meal, Ingredient


CHOICES1 = [
    ('M', 'Male'),
    ('F', 'Female')
]

CHOICES2 = [
    ('L', 'Lightly active (moderate exercise but sedentary job)'),
    ('M', 'Moderately active (intense exercise but sedentary job)'),
    ('V', 'Very active (moderate exercise and active job)'),
    ('E', 'Extra active (intense exercise and active job)')
]


class CaloriesCalculatorForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=CHOICES1, widget=forms.RadioSelect())
    job = forms.ChoiceField(choices=CHOICES2, widget=forms.RadioSelect())
    weight = forms.FloatField(help_text='Kg')
    goal_weight = forms.FloatField(help_text='Kg')
    goal_time_period = forms.IntegerField(help_text='Weeks')
    height = forms.FloatField(help_text='e.g. 5 feet 4 inch = 5.4')
    age = forms.IntegerField(help_text='Years')

    class Meta:
        model = Profile
        fields = ['gender', 'age', 'weight', 'height', 'job', 'goal_weight', 'goal_time_period']


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        exclude = ('ingredient_calories',)


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        exclude = ('meal_calories','meal_fat','meal_carbs','meal_protein')
