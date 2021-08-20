from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Recipe(models.Model):
    name = models.CharField(max_length=120)
    type = models.CharField(max_length=120)
    ingredients = models.JSONField()
    method = models.JSONField()
    summary = models.TextField(default="This is cool")
    date_created = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
