from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=255)
    protein = models.IntegerField()
    carbs = models.IntegerField()
    fat = models.IntegerField()
    ingredient_calories = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.ingredient_name


class Meal(models.Model):
    meal_name = models.CharField(max_length=255)
    veg = models.BooleanField()
    breakfast = models.BooleanField()
    lunch = models.BooleanField()
    dinner = models.BooleanField()
    snacks = models.BooleanField()
    ingredients = models.ManyToManyField('Ingredient', related_name='ingredientName')
    quantity = models.CharField(max_length=20, null=True)
    meal_method = models.CharField(max_length=2000000)
    meal_carbs = models.IntegerField(null=True, blank=True)
    meal_protein = models.IntegerField(null=True, blank=True)
    meal_fat = models.IntegerField(null=True, blank=True)
    meal_calories = models.IntegerField(null=True, blank=True)

    def get_ingredients(self):
        return ', '.join([i.ingredient_name for i in self.ingredients.all()])

    def __str__(self):
        return self.meal_name


class Dietplan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dietplan_name = models.CharField(max_length=255, null=True)
    breakfast = models.ManyToManyField(Meal, related_name='db')  # db means dietplan breakfast
    snacks1 = models.ManyToManyField(Meal, related_name='s1')
    lunch = models.ManyToManyField(Meal, related_name='dl')
    snacks2 = models.ManyToManyField(Meal, related_name='s2')
    dinner = models.ManyToManyField(Meal, related_name='dd')
    calories_slab = models.IntegerField(blank=True, null=True)

    def get_breakfast(self):  # this get function using to get all meals in breakfast and display them in admin panel under list using ','.join() but for meal meal we have to use object of mealnaem bnot for breakfast eg. m.meal_name for m in breakfast
        return ', '.join([m.meal_name for m in self.breakfast.all()])

    def get_snacks1(self):
        return ', '.join([m.meal_name for m in self.snacks1.all()])

    def get_lunch(self):
        return ', '.join([m.meal_name for m in self.lunch.all()])

    def get_snacks2(self):
        return ', '.join([m.meal_name for m in self.snacks2.all()])

    def get_dinner(self):
        return ', '.join([m.meal_name for m in self.dinner.all()])

    def create_dieplan(sender, instance, created, **kwargs):  # to create table automatically as user created
        if created:
            Dietplan.objects.create(user=instance)
    post_save.connect(create_dieplan, sender=User)
