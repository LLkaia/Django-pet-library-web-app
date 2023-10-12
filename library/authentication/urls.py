from django.urls import path
from authentication import views

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', views.users, name='users'),
    path('users/<int:user_id>/', views.concrete_user, name='concrete-user'),
    path('users/<int:user_id>/orders/', views.user_orders, name='user-orders'),
    path('users/create/', views.create_user, name='create-user'),
    path('users/create/<int:user_id>/', views.create_user, name='create-user'),
]