import os

import django
from faker import Faker


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library.settings")
django.setup()
from book.models import Book
from author.models import Author


fake = Faker()

for _ in range(50):
    book = Book.objects.create(name=fake.sentence(nb_words=3), description=fake.paragraph(),
                               date_of_release=fake.date_object(), date_of_issue=fake.date_object())
    author = Author.objects.create(name=fake.first_name(), surname=fake.last_name(), date_of_birth=fake.date_of_birth())
    author.books.add(book)
