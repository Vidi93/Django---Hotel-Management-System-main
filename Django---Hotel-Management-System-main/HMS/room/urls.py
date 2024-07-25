from django.urls import path
from . import views

urlpatterns = [
    path('booking/make/', views.booking_make, name='booking_make'),
    path('booking/my/', views.my_bookings, name='my_bookings'),
    path('booking/confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
]