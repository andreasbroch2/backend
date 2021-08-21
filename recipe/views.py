from django.shortcuts import get_object_or_404, render
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

def recipe_add_ingredients_view(request, id=id):
    obj = get_object_or_404(Recipe, id=id)
    form = RecipeForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
    context = {
        'form': form,
        'object': obj
    }
    return render(request, "add-ingredients.html", context)
# Create your views here.
def recipes(request):
    context = {
    'recipes': Recipe.objects.all()
    }
    return render(request, 'opskrifter.html', context)