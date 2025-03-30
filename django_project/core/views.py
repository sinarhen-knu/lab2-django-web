from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm


class TaskListView(ListView):
    model = Task
    template_name = 'core/task_list.html'
    context_object_name = 'tasks'


class TaskDetailView(DetailView):
    model = Task
    template_name = 'core/task_detail.html'
    context_object_name = 'task'


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'core/task_form.html'
    success_url = reverse_lazy('task-list')


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'core/task_form.html'
    success_url = reverse_lazy('task-list')


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'core/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')


def health_check(request):
    """A simple health check view to verify the application is running."""
    return render(request, 'core/health_check.html') 