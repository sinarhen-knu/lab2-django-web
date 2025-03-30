from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import MenuItem, Category, Ingredient


class MenuItemModelTest(TestCase):
    
    def setUp(self):
        category = Category.objects.create(name="Test Category")
        MenuItem.objects.create(
            name="Test Item",
            description="This is a test menu item",
            price=9.99,
            category=category,
            spice_level=1
        )
    
    def test_menuitem_creation(self):
        item = MenuItem.objects.get(name="Test Item")
        self.assertEqual(item.description, "This is a test menu item")
        self.assertEqual(float(item.price), 9.99)
    
    def test_menuitem_str_method(self):
        item = MenuItem.objects.get(name="Test Item")
        self.assertEqual(str(item), "Test Item")


class MenuItemViewsTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        # Create a test user
        User = get_user_model()
        self.user = User.objects.create_superuser(
            username='testadmin',
            email='admin@example.com',
            password='testpassword'
        )
        
        category = Category.objects.create(name="Test Category")
        self.menuitem = MenuItem.objects.create(
            name="Test Item",
            description="This is a test menu item",
            price=9.99,
            category=category,
            spice_level=1
        )
        self.list_url = reverse('menu-item-list')
        self.detail_url = reverse('menu-item-detail', args=[self.menuitem.id])
        self.create_url = reverse('menu-item-create')
        self.update_url = reverse('menu-item-update', args=[self.menuitem.id])
        self.delete_url = reverse('menu-item-delete', args=[self.menuitem.id])
        self.health_url = reverse('health-check')
    
    def test_menuitem_list_view_requires_login(self):
        # Test that unauthenticated request redirects to login
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 302)  # Redirects to login
        
        # Test that authenticated request succeeds
        self.client.login(username='testadmin', password='testpassword')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/admin/menu_item_list.html')
        self.assertContains(response, "Test Item")
    
    def test_menuitem_detail_view(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/menu_item_detail.html')
        self.assertContains(response, "Test Item")
    
    def test_menuitem_create_view_requires_login(self):
        # Test that unauthenticated request redirects to login
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)  # Redirects to login
        
        # Test that authenticated request succeeds
        self.client.login(username='testadmin', password='testpassword')
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/admin/menu_item_form.html')
        
        # Test POST with authenticated user
        category = Category.objects.get(name="Test Category")
        menuitem_data = {
            'name': 'New Item',
            'description': 'This is a new menu item',
            'price': 12.99,
            'category': category.id,
            'spice_level': 2,
            'ingredients': []  # Add empty ingredients list
        }
        response = self.client.post(self.create_url, menuitem_data)
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertTrue(MenuItem.objects.filter(name='New Item').exists())
    
    def test_menuitem_update_view_requires_login(self):
        # Test that unauthenticated request redirects to login
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 302)  # Redirects to login
        
        # Test that authenticated request succeeds
        self.client.login(username='testadmin', password='testpassword')
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/admin/menu_item_form.html')
        
        # Test POST with authenticated user
        category = Category.objects.get(name="Test Category")
        updated_data = {
            'name': 'Updated Item',
            'description': 'This menu item has been updated',
            'price': 14.99,
            'category': category.id,
            'spice_level': 3,
            'ingredients': []  # Add empty ingredients list
        }
        response = self.client.post(self.update_url, updated_data)
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.menuitem.refresh_from_db()
        self.assertEqual(self.menuitem.name, 'Updated Item')
        self.assertEqual(float(self.menuitem.price), 14.99)
    
    def test_menuitem_delete_view_requires_login(self):
        # Test that unauthenticated request redirects to login
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 302)  # Redirects to login
        
        # Test that authenticated request succeeds
        self.client.login(username='testadmin', password='testpassword')
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/admin/menu_item_confirm_delete.html')
        
        # Test POST (delete) with authenticated user
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertFalse(MenuItem.objects.filter(id=self.menuitem.id).exists())
    
    def test_health_check(self):
        response = self.client.get(self.health_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/health_check.html')


class MenuItemFormTest(TestCase):
    
    def test_valid_form(self):
        from .forms import MenuItemForm
        
        category = Category.objects.create(name="Form Test Category")
        data = {
            'name': 'Form Test Item',
            'description': 'This is a menu item created from a form test',
            'price': 8.99,
            'category': category.id,
            'spice_level': 1,
            'ingredients': [],
            'is_vegetarian': False,
            'is_vegan': False,
            'is_gluten_free': False,
            'is_available': True
        }
        form = MenuItemForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form(self):
        from .forms import MenuItemForm
        
        # Empty name (required field)
        data = {
            'name': '',
            'description': 'This is a menu item with no name',
            'price': 7.99,
            'spice_level': 1
        }
        form = MenuItemForm(data=data)
        self.assertFalse(form.is_valid()) 