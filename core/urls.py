
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('store.urls' , namespace='store')),
    path('accounts/' , include('accounts.urls' , namespace='accounts')),
    path('cart/' , include('cart.urls' , namespace='cart')),
    path('orders/' , include('orders.urls' , namespace='orders')),
    path('coupons/' , include('coupons.urls' , namespace='coupons')),

    #API
    path('api/', include(('api.urls', 'api'))),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)