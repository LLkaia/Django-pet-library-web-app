from django.contrib.auth.hashers import make_password
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from authentication.models import CustomUser
from book.models import Book
from library.forms import CustomRegistrationForm, BookFilterForm, CustomUserCreationForm
from django.contrib.auth import logout


def index(request):
    books = Book.objects.all()
    form = None
    if request.method == 'POST':
        form = BookFilterForm(request.POST)
        if form.is_valid():
            author = form.cleaned_data['author']
            name = form.cleaned_data['name']
            if author:
                books = books.filter(authors=author)
            if name:
                books = books.filter(name__icontains=name)
    data = {
        'title': 'Main page',
        'user': request.user,
        'books': books,
        'form': form,
    }
    return render(request, 'authentication/index.html', context=data)


def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomRegistrationForm()
    data = {
        'title': 'Register',
        'logout': False,
        'form': form,
    }
    return render(request, 'authentication/register.html', context=data)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    data = {
        'title': 'Log In',
        'logout': False,
        'form': form,
    }
    return render(request, 'authentication/login.html', data)


def logout_view(request):
    logout(request)
    return redirect('home')


def users(request):
    if request.user.role != 1:
        return HttpResponseForbidden
    users = CustomUser.get_all()
    data = {
        'title': 'Users',
        'all_users': users,
        'user': request.user,
    }
    return render(request, 'authentication/users.html', context=data)


def concrete_user(request, user_id):
    if request.user.role != 1:
        return HttpResponseForbidden
    user = CustomUser.get_by_id(user_id)
    data = {
        'title': f'{user.first_name} {user.last_name}',
        'one_user': user,
        'user': request.user,
    }
    return render(request, 'authentication/user.html', context=data)


def user_orders(request, user_id):
    if request.user.role != 1:
        return HttpResponseForbidden
    user = CustomUser.get_by_id(user_id)
    orders = user.books.all()
    data = {
        'title': f'{user.first_name} {user.last_name} --> orders',
        'orders': orders,
        'user': request.user,
    }
    return render(request, 'authentication/orders.html', context=data)

def create_user(request, user_id=0):
    if request.method == 'POST':
        if user_id == 0:
            form = CustomUserCreationForm(request.POST)
        else:
            user = CustomUser.get_by_id(user_id)
            form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.password = make_password(form.cleaned_data['password'])
            instance.save()
            return redirect('users')
    else:
        if user_id == 0:
            form = CustomUserCreationForm()
        else:
            user = CustomUser.get_by_id(user_id)
            form = CustomUserCreationForm(instance=user)
    data = {
        'title': 'Create/edit user',
        'user': request.user,
        'form': form,
    }
    return render(request, 'authentication/create.html', data)
