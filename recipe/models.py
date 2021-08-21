from django.db import models
from django.utils import timezone

class RecipeManager(models.Manager):
    def create_recipe(self, name, type, ingredients, method, summary, date_created, author):
        recipe = self.create(name=name, type=type, ingredients=ingredients, method=method, summary=summary, date_created=date_created, author=author)
        return recipe

class Ingredient(models.Model):
    name = models.CharField

class Recipe(models.Model):
    name = models.CharField(max_length=120)
    type = models.CharField(max_length=120)
    ingredients = models.ManyToManyField(Ingredient)
    method = models.JSONField(default=dict)
    summary = models.TextField(default="This is cool")
    date_created = models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.name

