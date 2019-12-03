from django.contrib import admin
from . models import Dietplan, Meal, Ingredient


class DietplanAdmin(admin.ModelAdmin):
    list_display = ('id', 'dietplan_name', 'get_breakfast', 'get_snacks1',
                    'get_lunch', 'get_snacks2', 'get_dinner', 'calories_slab')


class MealAdmin(admin.ModelAdmin):
    list_display = ('id', 'meal_name', 'veg', 'breakfast', 'lunch', 'dinner',
                    'snacks', 'get_ingredients', 'quantity', 'meal_method', 'meal_carbs', 'meal_protein', 'meal_fat', 'meal_calories')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient_name', 'protein', 'carbs', 'fat', 'ingredient_calories')


admin.site.register(Dietplan, DietplanAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(Ingredient, IngredientAdmin)
