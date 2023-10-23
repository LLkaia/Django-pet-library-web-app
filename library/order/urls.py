from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_orders, name='orders'),
    path('<int:order_id>/', views.order_detail, name='order-detail'),
    path('create/', views.create_order, name='create-order'),
    path('create/<int:book_id>', views.create_order, name='create-order-book'),
    path('close/<int:order_id>/', views.close_order, name='close-order'),
    path('delete/<int:order_id>/', views.delete_order, name='delete-order'),
]

