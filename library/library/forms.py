from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
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


class CustomUserEditingForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'middle_name', 'email',
                  'password', 'new_password', 'role', 'is_staff', 'is_superuser', 'is_active')

    def __init__(self, *args, **kwargs):
        exclude_field = kwargs.pop('exclude_field', False)
        super(CustomUserEditingForm, self).__init__(*args, **kwargs)
        if exclude_field:
            del self.fields['new_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        new_password = cleaned_data.get('new_password')
        if new_password:
            cleaned_data['password'] = make_password(new_password)
        else:
            cleaned_data['password'] = make_password(password)
        return cleaned_data


class BookCreationForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('name', 'description', 'date_of_release', 'date_of_issue', 'count')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'date_of_release': forms.DateInput(attrs={'type': 'date'}),
            'date_of_issue': forms.DateInput(attrs={'type': 'date'}),
        }


class BookFilterForm(forms.Form):
    author = forms.ModelChoiceField(queryset=Author.objects.all(), empty_label="All Authors", required=False)
    name = forms.CharField(max_length=128, required=False)


class AuthorCreationForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('name', 'surname', 'patronymic', 'date_of_birth', 'date_of_death', 'books')
        widgets = {
            'books': forms.CheckboxSelectMultiple,
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_of_death': forms.DateInput(attrs={'type': 'date'}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('book', 'plated_end_at')
        widgets = {
            'plated_end_at': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'book': 'Choose the book:',
            'plated_end_at': 'Planned date of return:',
        }
