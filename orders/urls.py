from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('payment/<int:order_id>/', views.order_payment_by_vodafone, name='payment_order'),
    path('payment/success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('admin/pdf/<int:order_id>/', views.admin_order_pdf, name='admin_order_pdf'),
]