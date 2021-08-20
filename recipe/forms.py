from django import forms

from .models import Recipe

class RecipeForm(forms.ModelForm):
    title       = forms.CharField(label='', 
                    widget=forms.TextInput(attrs={"placeholder": "Your title"}))
    type        = forms.CharField(
                        required=False, 
                        widget=forms.TextInput(attrs={"placeholder": "Your type"}))
    summary     = forms.Textarea()

    
    class Meta:
        model = Recipe
        fields = [
            'title',
            'type',
            'description'
        ]
