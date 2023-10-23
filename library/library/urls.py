from django.urls import path, include, re_path
from django.contrib import admin
from rest_framework import routers
from authentication.views import CustomUserViewSet
from order.views import OrderViewSet
from author import views as author_views
#from rest_framework.routers import DefaultRouter
from book.views import BookViewSet


router = routers.SimpleRouter()
router.register(r'user', CustomUserViewSet, basename='user')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'author', author_views.AuthorViewSet, basename='author')
router.register(r'book', BookViewSet, basename='book')

order_router = routers.SimpleRouter()
order_router.register(r'order', OrderViewSet, basename='customuser-order-detail')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/user/<int:user_id>/', include(order_router.urls)),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

    path('', include('authentication.urls')),
    path('books/', include('book.urls')),
    path('orders/', include('order.urls')),
    path('authors/', include('author.urls')),
]
