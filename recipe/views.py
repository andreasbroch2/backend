from django.shortcuts import render
from .models import Recipe
from .forms import RecipeForm

# Create your views here.
def recipe_create_view(request):
    form = RecipeForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = RecipeForm()
    context = {
        'form': form
    }
    return render(request, 'create-recipe.html', context)
    
# Create your views here.
def recipes(request):
    context = {
    'recipes': Recipe.objects.all()
    }
    return render(request, 'opskrifter.html', context)