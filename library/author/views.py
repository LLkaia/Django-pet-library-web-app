from author.models import Author
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from library.forms import AuthorForm


def all_authors(request):
    authors = Author.objects.all()
    data = {
        'title': 'Authors',
        'authors': authors,
    }
    return render(request, 'author/authors.html', context=data)


def create_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            messages.success(request, f'Author "{author.name}" has been created successfully.')
            return redirect('authors')
    else:
        form = AuthorForm()
    context = {'form': form, 'title': 'Create New Author'}
    return render(request, 'author/create_author.html', context)


def delete_author(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if not author.books.exists():
        author.delete()
        messages.success(request, f'Author "{author.name}" has been successfully closed.')
    else:
        messages.error(request, f'Author "{author.name}" is associated with books and cannot be closed.')

    return redirect('authors')
