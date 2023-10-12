from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_authors, name='authors'),
    path('create-author/', views.create_author, name='create_author'),
    path('delete-author/<int:pk>/', views.delete_author, name='delete_author'),
]
