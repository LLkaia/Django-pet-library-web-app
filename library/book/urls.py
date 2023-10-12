from django.urls import path
from book import views

urlpatterns = [
    path('<int:book_id>/', views.concrete_book, name='concrete-book'),
    path('create/', views.create_book, name='create-book'),
    path('create/<int:book_id>/', views.create_book, name='create-book'),
]