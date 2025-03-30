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
        # Public view URL
        self.detail_url = reverse('menu-item-detail', args=[self.menuitem.id])
        # Health check URL
        self.health_url = reverse('health-check')
    
    def test_public_menu_item_detail_view(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/menu_item_detail.html')
        self.assertContains(response, "Test Item")
    
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
            'is_vegetarian': False,
            'is_vegan': False,
            'is_gluten_free': False,
            'is_available': True
        }
        form = MenuItemForm(data=data)
        if not form.is_valid():
            print(f"Form errors: {form.errors}")
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