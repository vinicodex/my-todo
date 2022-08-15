from datetime import datetime
from sqlite3 import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from todo.forms import TodoForm
from todo.models import Todo

# Create your views here.
def signup_user(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('todos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Password does not match'})
        else:
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})

def login_user(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'User not found.'})
        else:
            login(request, user)
            return redirect('todos')

@login_required
def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect('loginuser')
    else:
        return redirect('logoutuser')

@login_required
def current_todos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True, completed=False)
    return render(request, 'todo/currenttodos.html', {'todos':todos}) 

@login_required
def completed_todos(request):
    todos = Todo.objects.filter(user=request.user, completed=True)
    return render(request, 'todo/completedtodos.html', {'todos':todos}) 

@login_required
def create_todos(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm})
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('todos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form':TodoForm, 'error':'Invalid data provided'})

@login_required
def view_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('todos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form, 'error':'Invalid request'})

@login_required
def complete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    print(todo)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.completed=True
        todo.save()
        return redirect('todos')

@login_required
def delete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('todos')
