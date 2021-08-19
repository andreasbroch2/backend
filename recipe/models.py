from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=120)
    type = models.TextField()
    ingredients = models.JSONField()
    method = models.JSONField()
    summary = models.TextField(default="This is cool")