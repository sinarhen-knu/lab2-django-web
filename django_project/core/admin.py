from django.contrib import admin
from .models import Category, MenuItem, Ingredient


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_vegetarian', 'is_vegan', 'is_gluten_free', 'spice_level', 'is_available')
    list_filter = ('category', 'is_vegetarian', 'is_vegan', 'is_gluten_free', 'spice_level', 'is_available')
    search_fields = ('name', 'description')
    filter_horizontal = ('ingredients',) 