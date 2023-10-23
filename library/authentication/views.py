from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from authentication.models import CustomUser
from book.models import Book
from library.forms import CustomRegistrationForm, BookFilterForm, CustomUserEditingForm
from django.contrib.auth import logout
from rest_framework import viewsets
from .serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def perform_create(self, serializer):
        password = self.request.data.get('password')
        hashed_password = make_password(password)
        serializer.validated_data['password'] = hashed_password
        serializer.save()

    def perform_update(self, serializer):
        password = self.request.data.get('password')
        if password:
            hashed_password = make_password(password)
            serializer.validated_data['password'] = hashed_password
        serializer.save()


def is_admin(user):
    return user.role == 1


def index(request):
    books = Book.objects.all()
    if request.method == 'POST':
        form = BookFilterForm(request.POST)
        if form.is_valid():
            author = form.cleaned_data['author']
            name = form.cleaned_data['name']
            if author:
                books = books.filter(authors=author)
            if name:
                books = books.filter(name__icontains=name)
    else:
        form = None
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


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id=0):
    if request.method == 'POST':
        if user_id == 0:
            form = CustomUserEditingForm(request.POST)
        else:
            user = CustomUser.get_by_id(user_id)
            form = CustomUserEditingForm(request.POST, instance=user)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.password = form.cleaned_data['password']
            instance.save()
            return redirect('users')
    else:
        if user_id == 0:
            form = CustomUserEditingForm(exclude_field=True)
        else:
            user = CustomUser.get_by_id(user_id)
            form = CustomUserEditingForm(instance=user)
    data = {
        'title': 'Create/edit user',
        'user': request.user,
        'form': form,
    }
    return render(request, 'authentication/create.html', data)


@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    if request.user.id != user_id:
        CustomUser.delete_by_id(user_id)
    return redirect('users')


@login_required
@user_passes_test(is_admin)
def users(request):
    all_users = CustomUser.get_all()
    data = {
        'title': 'Users',
        'all_users': all_users,
        'user': request.user,
    }
    return render(request, 'authentication/users.html', context=data)


@login_required
@user_passes_test(is_admin)
def concrete_user(request, user_id):
    user = CustomUser.get_by_id(user_id)
    data = {
        'title': f'{user.first_name} {user.last_name}',
        'one_user': user,
        'user': request.user,
    }
    return render(request, 'authentication/user.html', context=data)


@login_required
@user_passes_test(is_admin)
def user_orders(request, user_id):
    user = CustomUser.get_by_id(user_id)
    books = user.books.all()
    data = {
        'title': f'{user.first_name} {user.last_name} -- > Orders',
        'orders': books,
        'user': request.user,
    }
    return render(request, 'order/orders.html', context=data)
