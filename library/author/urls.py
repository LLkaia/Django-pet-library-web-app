from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_authors, name='authors'),
    path('create/', views.create_author, name='create-author'),
    path('edit/<int:author_id>', views.create_author, name='edit-author'),
    path('delete/<int:author_id>/', views.delete_author, name='delete-author'),
]
