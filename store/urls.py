from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    
  path('products/', views.list_product , name='list_product'),
]