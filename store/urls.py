from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    
  path('', views.list_product , name='list_product'),
  path('category/<slug:category_slug>/', views.list_product , name='product_by_category'),
  path('product/<slug:product_slug>/', views.product_detail , name='product_detail'),
  path('search/' , views.product_search , name='product_search')
]