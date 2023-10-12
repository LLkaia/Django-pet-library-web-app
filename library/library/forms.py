from django import forms
from django.contrib.auth.forms import UserCreationForm
from authentication.models import CustomUser
from author.models import Author
from order.models import Order
from book.models import Book


class CustomRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    middle_name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(max_length=100, required=True)
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label='Repeat password',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'middle_name', 'email', 'password1', 'password2')


class BookFilterForm(forms.Form):
    author = forms.ModelChoiceField(queryset=Author.objects.all(), empty_label="All Authors", required=False)
    name = forms.CharField(max_length=128, required=False)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['book']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'surname', 'patronymic', 'books']
        widgets = {
            'books': forms.CheckboxSelectMultiple,
        }

class BookCreationForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('name', 'description', 'date_of_release', 'date_of_issue', 'count')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'date_of_release': forms.DateInput(attrs={'type': 'date'}),
            'date_of_issue': forms.DateInput(attrs={'type': 'date'}),
        }

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'middle_name', 'email',
                  'password', 'role', 'is_staff', 'is_superuser', 'is_active')
