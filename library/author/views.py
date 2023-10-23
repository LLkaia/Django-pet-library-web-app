from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from authentication.views import is_admin
from author.models import Author
from django.shortcuts import render, redirect, get_object_or_404
from library.forms import AuthorCreationForm

from rest_framework import viewsets
from .models import Author
from .serializers import AuthorSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


@login_required
@user_passes_test(is_admin)
def all_authors(request):
    authors = Author.objects.all()
    data = {
        'title': 'Authors',
        'authors': authors,
    }
    return render(request, 'author/authors.html', context=data)


@login_required
@user_passes_test(is_admin)
def create_author(request, author_id=0):
    if request.user.role != 1:
        return HttpResponseForbidden
    if request.method == 'POST':
        if author_id == 0:
            form = AuthorCreationForm(request.POST)
        else:
            author = Author.get_by_id(author_id)
            form = AuthorCreationForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('authors')
    else:
        if author_id == 0:
            form = AuthorCreationForm()
        else:
            author = Author.get_by_id(author_id)
            form = AuthorCreationForm(instance=author)
    data = {
        'form': form,
        'title': 'Create/edit author',
        'user': request.user,
    }
    return render(request, 'author/create_author.html', data)


@login_required
@user_passes_test(is_admin)
def delete_author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    if not author.books.exists():
        author.delete()
    return redirect('authors')
