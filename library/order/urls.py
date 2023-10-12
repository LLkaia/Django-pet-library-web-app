from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_orders, name='orders'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('create/', views.create_order, name='create_order'),
    path('close/<int:order_id>/', views.close_order, name='close_order'),
]
