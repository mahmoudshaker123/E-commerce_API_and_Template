
from django.contrib import admin
from django.urls import path , include



urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('accounts.urls' , namespace='accounts')),
    path('store/' , include('store.urls' , namespace='store')),
]
