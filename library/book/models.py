from django.core.exceptions import ValidationError
from django.db import models


def validate_description(value):
    if len(value) < 8:
        raise ValidationError(
            'Description is too short.'
        )


class Book(models.Model):
    name = models.CharField(blank=True, max_length=128)
    description = models.CharField(blank=True, max_length=256, validators=[validate_description])
    count = models.IntegerField(default=10)
    id = models.AutoField(primary_key=True)
    date_of_release = models.DateField(null=True, blank=True, default=None)
    date_of_issue = models.DateField(null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"Book(id={self.id})"

    @staticmethod
    def get_by_id(book_id):
        book = Book.objects.filter(pk=book_id).first()
        return book if book else None

    @staticmethod
    def delete_by_id(book_id):
        book = Book.objects.filter(pk=book_id)
        if not book:
            return False
        book.delete()
        return True

    @staticmethod
    def create(name, description, count=10, authors=None):
        if len(name) > 128:
            return None

        book = Book()
        book.name = name
        book.description = description
        book.count = count
        if (authors is not None):
            for elem in authors:
                book.authors.add(elem)
        book.save()
        return book

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'count': self.count
        }

    def update(self, name=None, description=None, count=None):
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if count is not None:
            self.count = count
        self.save()

    def add_authors(self, authors):
        for author in authors:
            self.authors.add(author)

    def remove_authors(self, authors):
        for author in authors:
            self.authors.remove(author)

    @staticmethod
    def get_all():
        return Book.objects.all()
