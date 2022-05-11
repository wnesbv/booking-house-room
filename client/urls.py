

from django.urls import path
from . import views


urlpatterns = [
    path('', views.client, name='client'),
    path('my_appointment/', views.client, name='client'),
    path('quick_appointmnet/', views.quick_appointmnet, name='quick_appointmnet'),
    path('update/<indicator>/', views.appointment_book, name='appointment_update'),
]
