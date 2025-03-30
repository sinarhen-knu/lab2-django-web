from django import forms
from .models import Category, MenuItem, Ingredient


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'parent']


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name']


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'image', 'category', 'ingredients', 
                 'is_vegetarian', 'is_vegan', 'is_gluten_free', 'spice_level', 'is_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'ingredients': forms.CheckboxSelectMultiple(),
        }


class MenuFilterForm(forms.Form):
    SPICE_CHOICES = [
        ('', 'Any spice level'),
        (1, 'Mild'),
        (2, 'Medium'),
        (3, 'Spicy'),
        (4, 'Very Spicy'),
        (5, 'Extreme'),
    ]
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All categories"
    )
    is_vegetarian = forms.BooleanField(required=False)
    is_vegan = forms.BooleanField(required=False)
    is_gluten_free = forms.BooleanField(required=False)
    spice_level = forms.ChoiceField(choices=SPICE_CHOICES, required=False)
    min_price = forms.DecimalField(max_digits=6, decimal_places=2, required=False)
    max_price = forms.DecimalField(max_digits=6, decimal_places=2, required=False)
    search = forms.CharField(required=False) 