"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from pages import views
from recipe import views as recipeviews

urlpatterns = [
    path('', include('pages.urls')),
    path('home/', views.home_view, name='home'),
    path('opskrifter/', views.opskrifter, name='opskrifter'),
    path('admin/', admin.site.urls),
    path('celery-progress/', include('celery_progress.urls')),
    path('recipes/', recipeviews.recipes, name="recipes"), 
    path('create-recipe/', recipeviews.recipe_create_view, name="create-recipe"),
    path('add-ingredients/<int:id>', recipeviews.recipe_add_ingredients_view, name="add-ingredients")
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
