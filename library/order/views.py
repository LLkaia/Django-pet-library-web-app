from django.shortcuts import render, redirect, get_object_or_404

from order.models import Order

from library.forms import OrderForm
import datetime


def all_orders(request):
    orders = Order.get_all()
    data = {
        'title': 'Orders',
        'orders': orders,
        'user': request.user,
    }
    return render(request, 'order/orders.html', context=data)


def order_detail(request, order_id):
    order = Order.get_by_id(order_id)
    data = {
        'title': 'Order details',
        'order': order,
        'user': request.user,
    }
    return render(request, 'order/order_detail.html', context=data)


def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('orders')
    else:
        form = OrderForm()

    context = {'form': form, 'title': 'Create Order'}
    return render(request, 'order/create_order.html', context)


def close_order(request, order_id):
    request.user.role = 1
    order = get_object_or_404(Order, id=order_id)
    if not order.is_closed:
        order.is_closed = True
        order.end_at = datetime.datetime.now()
        order.save()
    return redirect('orders')
