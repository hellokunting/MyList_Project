from django.shortcuts import render, redirect
from django.http import HttpResponse
from todolist_app.models import TaskList
from todolist_app.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            form.save()
            messages.success(request, ("New Task Added!"))
        return redirect('todolist')
    else:
        all_tasks = TaskList.objects.filter(owner=request.user)
        paginator = Paginator(all_tasks, 5)
        page = request.GET.get('pg')
        all_tasks = paginator.get_page(page)
        return render(request, 'todolist.html', {'all_tasks': all_tasks})


def delete_task(request, task_id): 
    task = TaskList.objects.get(pk=task_id)
    if task.owner == request.user:
        task.delete()
    else:
        messages.error(request, ("Access Restricted. You are not allowed to visit this page."))
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    # return redirect('todolist')


def edit_task(request, task_id):
    if request.method == "POST":
        task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, ("Task has been edited!"))
        return redirect('todolist')
    else:
        task_obj = TaskList.objects.get(pk=task_id)
        return render(request, 'edit.html', {'task_obj': task_obj})


def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.owner == request.user:
        task.done = True
        task.save()
    else:
        messages.error(request, ("Access Restricted. You are not allowed to visit this page."))
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    task.done = False
    task.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def contact(request):
    context = {
        'contact_text': "Contact Us",
    }
    return render(request, 'contact.html', context)


def about(request):
    context = {
        'about_text': "About Page",
    }
    return render(request, 'about.html', context)


def index(request):
    context = {
        'index_text': "Index Page",
    }
    return render(request, 'index.html', context)
