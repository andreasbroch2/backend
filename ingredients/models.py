from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=120)
    type = models.TextField()
    price = models.TextField()
    summary = models.TextField(default="This is cool")