from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Category, MenuItem, Ingredient
from .forms import CategoryForm, MenuItemForm, IngredientForm, MenuFilterForm


def home(request):
    """Home page view showing featured menu items and categories."""
    categories = Category.objects.filter(parent=None)
    featured_items = MenuItem.objects.filter(is_available=True)[:6]
    
    return render(request, 'core/home.html', {
        'categories': categories,
        'featured_items': featured_items
    })


def menu_list(request):
    """Menu listing with advanced filtering."""
    menu_items = MenuItem.objects.filter(is_available=True)
    form = MenuFilterForm(request.GET)
    
    if form.is_valid():
        # Apply filters based on form data
        if form.cleaned_data.get('category'):
            menu_items = menu_items.filter(category=form.cleaned_data['category'])
        
        if form.cleaned_data.get('is_vegetarian'):
            menu_items = menu_items.filter(is_vegetarian=True)
        
        if form.cleaned_data.get('is_vegan'):
            menu_items = menu_items.filter(is_vegan=True)
        
        if form.cleaned_data.get('is_gluten_free'):
            menu_items = menu_items.filter(is_gluten_free=True)
        
        if form.cleaned_data.get('spice_level'):
            menu_items = menu_items.filter(spice_level=form.cleaned_data['spice_level'])
        
        if form.cleaned_data.get('min_price'):
            menu_items = menu_items.filter(price__gte=form.cleaned_data['min_price'])
        
        if form.cleaned_data.get('max_price'):
            menu_items = menu_items.filter(price__lte=form.cleaned_data['max_price'])
        
        if form.cleaned_data.get('search'):
            query = form.cleaned_data['search']
            menu_items = menu_items.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(ingredients__name__icontains=query)
            ).distinct()
    
    categories = Category.objects.filter(parent=None)
    
    return render(request, 'core/menu_list.html', {
        'menu_items': menu_items,
        'categories': categories,
        'form': form
    })


def category_detail(request, slug):
    """View menu items in a specific category."""
    category = get_object_or_404(Category, slug=slug)
    menu_items = MenuItem.objects.filter(category=category, is_available=True)
    subcategories = Category.objects.filter(parent=category)
    
    return render(request, 'core/category_detail.html', {
        'category': category,
        'menu_items': menu_items,
        'subcategories': subcategories
    })


def menu_item_detail(request, pk):
    """Detailed view of a menu item."""
    menu_item = get_object_or_404(MenuItem, pk=pk)
    related_items = MenuItem.objects.filter(category=menu_item.category).exclude(pk=pk)[:4]
    
    return render(request, 'core/menu_item_detail.html', {
        'menu_item': menu_item,
        'related_items': related_items
    })


# Admin views for managing categories
class CategoryListView(ListView):
    model = Category
    template_name = 'core/admin/category_list.html'
    context_object_name = 'categories'


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'core/admin/category_form.html'
    success_url = reverse_lazy('category-list')


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'core/admin/category_form.html'
    success_url = reverse_lazy('category-list')


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'core/admin/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')


# Admin views for managing menu items
class MenuItemListView(ListView):
    model = MenuItem
    template_name = 'core/admin/menu_item_list.html'
    context_object_name = 'menu_items'


class MenuItemCreateView(CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'core/admin/menu_item_form.html'
    success_url = reverse_lazy('menu-item-list')


class MenuItemUpdateView(UpdateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'core/admin/menu_item_form.html'
    success_url = reverse_lazy('menu-item-list')


class MenuItemDeleteView(DeleteView):
    model = MenuItem
    template_name = 'core/admin/menu_item_confirm_delete.html'
    success_url = reverse_lazy('menu-item-list')


def health_check(request):
    """A simple health check view to verify the application is running."""
    return render(request, 'core/health_check.html')


def css_debug(request):
    """Debug view to check CSS loading."""
    from django.conf import settings
    import os
    
    # List the static directories
    staticfiles_dirs = settings.STATICFILES_DIRS
    static_root = settings.STATIC_ROOT
    
    # Check if the CSS file exists
    css_path = os.path.join(static_root, 'css', 'output.css')
    css_exists = os.path.exists(css_path)
    
    # If it exists, read first few lines
    css_content = ""
    if css_exists:
        with open(css_path, 'r') as f:
            css_content = f.read(500)  # First 500 characters
    
    context = {
        'staticfiles_dirs': staticfiles_dirs,
        'static_root': static_root,
        'css_exists': css_exists,
        'css_path': css_path,
        'css_content': css_content,
        'debug': settings.DEBUG,
    }
    
    return render(request, 'debug/css_debug.html', context) 