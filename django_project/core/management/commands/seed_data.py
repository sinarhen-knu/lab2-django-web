from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Category, MenuItem, Ingredient
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seeds the database with initial data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        
        with transaction.atomic():
            self.create_categories()
            self.create_ingredients()
            self.create_menu_items()
            
        self.stdout.write(self.style.SUCCESS('Data seeding completed successfully!'))
    
    def create_categories(self):
        self.stdout.write('Creating categories...')
        
        # Main categories
        appetizers = Category.objects.create(name='Appetizers', description='Starters and small plates')
        main_courses = Category.objects.create(name='Main Courses', description='Main dishes and entrees')
        desserts = Category.objects.create(name='Desserts', description='Sweet treats to end your meal')
        drinks = Category.objects.create(name='Drinks', description='Beverages and cocktails')
        
        # Sub-categories
        Category.objects.create(name='Soups', description='Warm and comforting soups', parent=appetizers)
        Category.objects.create(name='Salads', description='Fresh and healthy salads', parent=appetizers)
        
        Category.objects.create(name='Pasta', description='Italian pasta dishes', parent=main_courses)
        Category.objects.create(name='Seafood', description='Fresh seafood dishes', parent=main_courses)
        Category.objects.create(name='Steaks', description='Premium cuts of meat', parent=main_courses)
        Category.objects.create(name='Vegetarian', description='Meat-free main courses', parent=main_courses)
        
        Category.objects.create(name='Cakes', description='Delicious cake slices', parent=desserts)
        Category.objects.create(name='Ice Cream', description='Cold and creamy treats', parent=desserts)
        
        Category.objects.create(name='Hot Drinks', description='Coffee, tea and more', parent=drinks)
        Category.objects.create(name='Cold Drinks', description='Refreshing cold beverages', parent=drinks)
        Category.objects.create(name='Alcoholic Drinks', description='Beer, wine and cocktails', parent=drinks)
        
        self.stdout.write(self.style.SUCCESS(f'Created {Category.objects.count()} categories'))
    
    def create_ingredients(self):
        self.stdout.write('Creating ingredients...')
        
        ingredients = [
            # Proteins
            'Chicken', 'Beef', 'Pork', 'Salmon', 'Tuna', 'Shrimp', 'Tofu',
            # Vegetables
            'Tomato', 'Lettuce', 'Onion', 'Garlic', 'Bell Pepper', 'Carrot', 'Broccoli',
            'Spinach', 'Mushroom', 'Zucchini', 'Cucumber', 'Avocado',
            # Grains/Starches
            'Rice', 'Pasta', 'Potato', 'Bread', 'Quinoa',
            # Dairy
            'Cheese', 'Milk', 'Cream', 'Butter', 'Yogurt',
            # Others
            'Olive Oil', 'Lemon', 'Lime', 'Basil', 'Cilantro', 'Parsley',
            'Salt', 'Pepper', 'Sugar', 'Flour', 'Egg'
        ]
        
        for name in ingredients:
            Ingredient.objects.create(name=name)
            
        self.stdout.write(self.style.SUCCESS(f'Created {Ingredient.objects.count()} ingredients'))
    
    def create_menu_items(self):
        self.stdout.write('Creating menu items...')
        
        # Helper function to get category by name
        def get_category(name):
            return Category.objects.get(name=name)
        
        # Helper function to get ingredients by names
        def get_ingredients(*names):
            return [Ingredient.objects.get(name=name) for name in names]
        
        # Appetizers
        soups_category = get_category('Soups')
        salads_category = get_category('Salads')
        
        # Create tomato soup
        tomato_soup = MenuItem.objects.create(
            name='Tomato Basil Soup',
            description='Creamy tomato soup with fresh basil',
            price=Decimal('6.99'),
            category=soups_category,
            is_vegetarian=True,
            is_vegan=False,
            is_gluten_free=True,
            spice_level=1
        )
        tomato_soup.ingredients.add(*get_ingredients('Tomato', 'Garlic', 'Basil', 'Cream', 'Salt', 'Pepper', 'Olive Oil'))
        
        # Create caesar salad
        caesar_salad = MenuItem.objects.create(
            name='Caesar Salad',
            description='Classic Caesar salad with homemade dressing and croutons',
            price=Decimal('8.99'),
            category=salads_category,
            is_vegetarian=True,
            is_vegan=False,
            is_gluten_free=False,
            spice_level=1
        )
        caesar_salad.ingredients.add(*get_ingredients('Lettuce', 'Cheese', 'Bread', 'Olive Oil', 'Lemon', 'Garlic', 'Egg'))
        
        # Main Courses
        pasta_category = get_category('Pasta')
        seafood_category = get_category('Seafood')
        steaks_category = get_category('Steaks')
        vegetarian_category = get_category('Vegetarian')
        
        # Create pasta dish
        pasta_dish = MenuItem.objects.create(
            name='Spaghetti Carbonara',
            description='Classic Italian pasta with creamy egg sauce, pancetta and parmesan',
            price=Decimal('14.99'),
            category=pasta_category,
            is_vegetarian=False,
            is_vegan=False,
            is_gluten_free=False,
            spice_level=1
        )
        pasta_dish.ingredients.add(*get_ingredients('Pasta', 'Egg', 'Cheese', 'Pork', 'Garlic', 'Pepper'))
        
        # Create seafood dish
        seafood_dish = MenuItem.objects.create(
            name='Grilled Salmon',
            description='Fresh salmon fillet grilled to perfection with lemon butter sauce',
            price=Decimal('19.99'),
            category=seafood_category,
            is_vegetarian=False,
            is_vegan=False,
            is_gluten_free=True,
            spice_level=1
        )
        seafood_dish.ingredients.add(*get_ingredients('Salmon', 'Lemon', 'Butter', 'Garlic', 'Salt', 'Pepper', 'Olive Oil'))
        
        # Create steak dish
        steak_dish = MenuItem.objects.create(
            name='Ribeye Steak',
            description='Prime 10oz ribeye steak cooked to your preference',
            price=Decimal('29.99'),
            category=steaks_category,
            is_vegetarian=False,
            is_vegan=False,
            is_gluten_free=True,
            spice_level=2
        )
        steak_dish.ingredients.add(*get_ingredients('Beef', 'Butter', 'Salt', 'Pepper', 'Garlic'))
        
        # Create vegetarian dish
        vegetarian_dish = MenuItem.objects.create(
            name='Mushroom Risotto',
            description='Creamy arborio rice with wild mushrooms and parmesan',
            price=Decimal('15.99'),
            category=vegetarian_category,
            is_vegetarian=True,
            is_vegan=False,
            is_gluten_free=True,
            spice_level=1
        )
        vegetarian_dish.ingredients.add(*get_ingredients('Rice', 'Mushroom', 'Cheese', 'Butter', 'Garlic', 'Onion'))
        
        # Desserts
        cakes_category = get_category('Cakes')
        ice_cream_category = get_category('Ice Cream')
        
        # Create cake
        chocolate_cake = MenuItem.objects.create(
            name='Chocolate Lava Cake',
            description='Warm chocolate cake with a molten center, served with vanilla ice cream',
            price=Decimal('9.99'),
            category=cakes_category,
            is_vegetarian=True,
            is_vegan=False,
            is_gluten_free=False,
            spice_level=1
        )
        chocolate_cake.ingredients.add(*get_ingredients('Flour', 'Sugar', 'Egg', 'Butter', 'Milk'))
        
        # Create ice cream
        ice_cream = MenuItem.objects.create(
            name='Artisanal Gelato Trio',
            description='Three scoops of our homemade gelato in your choice of flavors',
            price=Decimal('7.99'),
            category=ice_cream_category,
            is_vegetarian=True,
            is_vegan=False,
            is_gluten_free=True,
            spice_level=1
        )
        ice_cream.ingredients.add(*get_ingredients('Milk', 'Cream', 'Sugar', 'Egg'))
        
        # Drinks
        hot_drinks_category = get_category('Hot Drinks')
        cold_drinks_category = get_category('Cold Drinks')
        alcoholic_drinks_category = get_category('Alcoholic Drinks')
        
        # Create hot drink
        hot_drink = MenuItem.objects.create(
            name='Cappuccino',
            description='Espresso with steamed milk and foam',
            price=Decimal('4.99'),
            category=hot_drinks_category,
            is_vegetarian=True,
            is_vegan=False,
            is_gluten_free=True,
            spice_level=1
        )
        hot_drink.ingredients.add(*get_ingredients('Milk'))
        
        # Create cold drink
        cold_drink = MenuItem.objects.create(
            name='Fresh Lemonade',
            description='Freshly squeezed lemons with sugar and ice',
            price=Decimal('3.99'),
            category=cold_drinks_category,
            is_vegetarian=True,
            is_vegan=True,
            is_gluten_free=True,
            spice_level=1
        )
        cold_drink.ingredients.add(*get_ingredients('Lemon', 'Sugar'))
        
        # Create alcoholic drink
        alcoholic_drink = MenuItem.objects.create(
            name='Classic Mojito',
            description='Rum, fresh mint, lime, sugar, and soda water',
            price=Decimal('9.99'),
            category=alcoholic_drinks_category,
            is_vegetarian=True,
            is_vegan=True,
            is_gluten_free=True,
            spice_level=1
        )
        alcoholic_drink.ingredients.add(*get_ingredients('Lime', 'Sugar'))
        
        self.stdout.write(self.style.SUCCESS(f'Created {MenuItem.objects.count()} menu items')) 