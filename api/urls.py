from django.urls import path
from . import views



app_name = 'api'

urlpatterns = [
    path('category/' , views.category_api , name='category_api'),
    path('category/<slug:slug>/' , views.category_api , name='category_api_detail'),
    path('products/' , views.product_api , name='product_api'),
    path('products/<slug:slug>/' , views.product_api , name='product_api_detail'),

    path('register/' , views.register_api , name='register_api'),

    path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),
    path('logout/' , views.logout , name='logout_api'),

   
]


