from django.test import TestCase, Client
from django.urls import reverse
from .models import Task


class TaskModelTest(TestCase):
    
    def setUp(self):
        Task.objects.create(
            title="Test Task",
            description="This is a test task",
            status="pending"
        )
    
    def test_task_creation(self):
        task = Task.objects.get(title="Test Task")
        self.assertEqual(task.description, "This is a test task")
        self.assertEqual(task.status, "pending")
    
    def test_task_str_method(self):
        task = Task.objects.get(title="Test Task")
        self.assertEqual(str(task), "Test Task")


class TaskViewsTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task",
            status="pending"
        )
        self.list_url = reverse('task-list')
        self.detail_url = reverse('task-detail', args=[self.task.id])
        self.create_url = reverse('task-create')
        self.update_url = reverse('task-update', args=[self.task.id])
        self.delete_url = reverse('task-delete', args=[self.task.id])
        self.health_url = reverse('health-check')
    
    def test_task_list_view(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/task_list.html')
        self.assertContains(response, "Test Task")
    
    def test_task_detail_view(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/task_detail.html')
        self.assertContains(response, "Test Task")
    
    def test_task_create_view(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/task_form.html')
        
        # Test POST
        task_data = {
            'title': 'New Task',
            'description': 'This is a new task',
            'status': 'in_progress'
        }
        response = self.client.post(self.create_url, task_data)
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertTrue(Task.objects.filter(title='New Task').exists())
    
    def test_task_update_view(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/task_form.html')
        
        # Test POST
        updated_data = {
            'title': 'Updated Task',
            'description': 'This task has been updated',
            'status': 'completed'
        }
        response = self.client.post(self.update_url, updated_data)
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertEqual(self.task.status, 'completed')
    
    def test_task_delete_view(self):
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/task_confirm_delete.html')
        
        # Test POST (delete)
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())
    
    def test_health_check(self):
        response = self.client.get(self.health_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/health_check.html')


class TaskFormTest(TestCase):
    
    def test_valid_form(self):
        from .forms import TaskForm
        
        data = {
            'title': 'Form Test Task',
            'description': 'This is a task created from a form test',
            'status': 'in_progress'
        }
        form = TaskForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form(self):
        from .forms import TaskForm
        
        # Empty title (required field)
        data = {
            'title': '',
            'description': 'This is a task with no title',
            'status': 'pending'
        }
        form = TaskForm(data=data)
        self.assertFalse(form.is_valid()) 