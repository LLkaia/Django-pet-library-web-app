from django.db import models, DataError

from authentication.models import CustomUser
from book.models import Book


class Order(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)
    end_at = models.DateTimeField(default=None, null=True, blank=True)
    plated_end_at = models.DateTimeField(default=None, null=True)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        end_at_str = f"'{self.end_at}'" if self.end_at is not None else 'None'
        return f"'id': {self.id}, 'user': CustomUser(id={self.user.id}), 'book': Book(id={self.book.id}), 'created_at': '{self.created_at}', 'end_at': {end_at_str}, 'plated_end_at': '{self.plated_end_at}'"

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id})'

    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.id,
            'user_id': self.user.id,
            'created_at': int(self.created_at.timestamp()),
            'end_at': int(self.end_at.timestamp()) if self.end_at else None,
            'plated_end_at': int(self.plated_end_at.timestamp())
        }

    @staticmethod
    def create(user, book, plated_end_at):
        orders = Order.objects.all()
        books = set()
        for order in orders:
            if not order.end_at:
                books.add(order.book.id)
        if book.id in books and book.count == 1:
            return None
        try:
            order = Order(user=user, book=book, plated_end_at=plated_end_at)
            order.save()
            return order
        except ValueError:
            return None
        except DataError:
            return None

    @staticmethod
    def get_by_id(order_id):
        try:
            return Order.objects.get(pk=order_id)
        except:
            return None

    def update(self, plated_end_at=None, end_at=None):
        if plated_end_at != None:
            self.plated_end_at = plated_end_at
        if end_at != None:
            self.end_at = end_at
        self.save()

    @staticmethod
    def get_all():
        return Order.objects.all()

    @staticmethod
    def get_not_returned_books():
        return Order.objects.filter(end_at=None).values()

    @staticmethod
    def delete_by_id(order_id):
        try:
            a = Order.objects.get(pk=order_id)
        except:
            return False
        else:
            a.delete()
            return True
