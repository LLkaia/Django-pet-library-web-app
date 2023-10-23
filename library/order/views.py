from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, timedelta
import datetime
from rest_framework import viewsets

from authentication.models import CustomUser
from authentication.views import is_admin
from book.models import Book
from order.models import Order
from library.forms import OrderForm
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id', None)
        if user_id:
            return Order.objects.filter(user=user_id)
        else:
            return Order.objects.all()

    def perform_create(self, serializer):
        user_id = self.kwargs.get('user_id', None)
        if user_id:
            user = CustomUser.get_by_id(user_id)
            serializer.save(user=user)
        else:
            serializer.save()


@login_required
def all_orders(request):
    orders = Order.get_all()
    data = {
        'title': 'Orders',
        'orders': orders,
        'user': request.user,
    }
    return render(request, 'order/orders.html', context=data)


@login_required
def order_detail(request, order_id):
    order = Order.get_by_id(order_id)
    data = {
        'title': 'Order details',
        'order': order,
        'user': request.user,
    }
    return render(request, 'order/order_detail.html', context=data)


@login_required
def create_order(request, book_id=0):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('orders')
    else:
        today = date.today()
        default_date = today + timedelta(days=14)
        if book_id == 0:
            form = OrderForm(initial={'plated_end_at': default_date})
        else:
            book = Book.get_by_id(book_id)
            form = OrderForm(initial={'plated_end_at': default_date, 'book': book})
    context = {'form': form, 'title': 'Create Order'}
    return render(request, 'order/create_order.html', context)


@login_required
@user_passes_test(is_admin)
def close_order(request, order_id):
    order = Order.get_by_id(order_id)
    order.end_at = datetime.datetime.now()
    order.is_closed = True
    order.save()
    return redirect('orders')


@login_required
@user_passes_test(is_admin)
def delete_order(request, order_id):
    Order.delete_by_id(order_id)
    return redirect('orders')