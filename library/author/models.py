from django.db import models, transaction
from django.db.utils import DataError
import book.models


class Author(models.Model):
    name = models.CharField(blank=True, max_length=20)
    surname = models.CharField(blank=True, max_length=20)
    patronymic = models.CharField(blank=True, max_length=20)
    books = models.ManyToManyField(book.models.Book, related_name='authors', blank=True)
    id = models.AutoField(primary_key=True)
    date_of_birth = models.DateField(null=True, blank=True, default=None)
    date_of_death = models.DateField(null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.name} {self.surname} {self.patronymic}"

    def __repr__(self):
        return f"Author(id={self.pk})"

    @staticmethod
    def get_by_id(author_id):
        author = Author.objects.filter(pk=author_id).first()
        return author if author else None

    @staticmethod
    def delete_by_id(author_id):
        author = Author.objects.filter(pk=author_id)
        if not author:
            return False
        author.delete()
        return True

    @staticmethod
    def create(name, surname, patronymic):
        try:
            author = Author(name=name, surname=surname, patronymic=patronymic)
            author.save()
            return author
        except DataError:
            return None

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'surname': self.surname, 'patronymic': self.patronymic}

    def update(self,
               name=None,
               surname=None,
               patronymic=None):
        try:
            with transaction.atomic():
                self.name = name if name else self.name
                self.surname = surname if surname else self.surname
                self.patronymic = patronymic if patronymic else self.patronymic
                self.save()
        except DataError:
            return None

    @staticmethod
    def get_all():
        return Author.objects.all()
