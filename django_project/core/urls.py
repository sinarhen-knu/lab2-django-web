from django.urls import path
from . import views

urlpatterns = [
    # Public views
    path('', views.home, name='home'),
    path('menu/', views.menu_list, name='menu-list'),
    path('category/<slug:slug>/', views.category_detail, name='category-detail'),
    path('menu-item/<int:pk>/', views.menu_item_detail, name='menu-item-detail'),
    
    # Admin views for categories
    path('admin/categories/', views.CategoryListView.as_view(), name='category-list'),
    path('admin/categories/new/', views.CategoryCreateView.as_view(), name='category-create'),
    path('admin/categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('admin/categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
    
    # Admin views for menu items
    path('admin/menu-items/', views.MenuItemListView.as_view(), name='menu-item-list'),
    path('admin/menu-items/new/', views.MenuItemCreateView.as_view(), name='menu-item-create'),
    path('admin/menu-items/<int:pk>/edit/', views.MenuItemUpdateView.as_view(), name='menu-item-update'),
    path('admin/menu-items/<int:pk>/delete/', views.MenuItemDeleteView.as_view(), name='menu-item-delete'),
    
    # Health check
    path('health/', views.health_check, name='health-check'),
    
    # Debug routes
    path('css-debug/', views.css_debug, name='css-debug'),
] 