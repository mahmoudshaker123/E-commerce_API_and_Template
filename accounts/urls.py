from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.register , name='register'),
    path('login/' , views.login , name='login'),
    path('activate/<uidb64>/<token>/' , views.activate , name='activate'),
]