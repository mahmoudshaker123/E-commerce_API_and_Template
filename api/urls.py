from django.urls import path
from . import views


app_name = 'api'

urlpatterns = [
    path('category/' , views.category_api , name='category_api'),
    path('category/<slug:slug>/' , views.category_api , name='category_api_detail'),
    path('products/' , views.product_api , name='product_api'),
]


