from django.shortcuts import render
from models import Recipe


# Create your views here.
def recipes(request):
    context = {
    'recipes': Recipe.objects.all()
    }
    return render(request, 'opskrifter.html', context)