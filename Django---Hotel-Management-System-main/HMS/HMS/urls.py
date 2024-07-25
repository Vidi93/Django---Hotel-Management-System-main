from django.contrib import admin
from django.urls import path
from room import views as room_views
from accounts.views import *
from room.views import *
from hotel.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),

    path('login/', login_page, name="login"),
    path('logout/', logout_user, name="logout"),
    path('register/', register_page, name="register"),

    path('guests/', guests, name="guests"),
    path('employees/', employees, name="employees"),
    path('events/', events, name="events"),
    path('bookings/', bookings, name="bookings"),
    path('rooms/', rooms, name="rooms"),
    path('room-services/', room_services, name="room-services"),
    path('announcements/', announcements, name="announcements"),
    path('refunds/', refunds, name="refunds"),
    path('storage/', storage, name="storage"),

    path('tasks/', tasks, name="tasks"),
    path('current-room-services/', current_room_services,
         name="current-room-services"),
    path('request-refund/', request_refund, name="request-refund"),
    path('event-profile/<str:id>/', event_profile, name="event-profile"),
    path('event-edit/<str:pk>/', event_edit, name="event-edit"),
    path('add-room/', add_room, name="add-room"),

    path('employee-profile/<str:pk>/', employee_details, name="employee-profile"),
    path('employee-edit/<str:pk>/', employee_details_edit, name="employee-edit"),
    path('employee-add/', add_employee, name="add-employee"),

    path('guest-edit/<str:pk>', guest_edit, name="guest-edit"),
    path('guest-profile/<str:pk>', guest_profile, name="guest-profile"),
    path('room-profile/<str:id>/', room_profile, name="room-profile"),
    path('room-edit/<str:pk>/', room_edit, name="room-edit"),
    path('error/', error, name="error"),

    path('booking-make/', booking_make, name="booking-make"),
    path('booking-make/', room_views.booking_make, name='booking-make'),
    path('booking-confirmation/<int:booking_id>/', room_views.booking_confirmation, name='booking_confirmation'),
    path('payment/', payment, name="payment"),
    path('verify/', verify, name="verify"),

    path('deleteStorage/<str:pk>/', deleteStorage, name="deleteStorage"),
    path('deleteFoodMenu/<str:pk>/', deleteFoodMenu, name="deleteFoodMenu"),
    path('food-menu/', food_menu, name="food-menu"),
    path('food-menu/<str:pk>/', food_menu_edit, name="food-menu-edit"),

    path('createEvent/', createEvent, name="createEvent"),
    path('deleteEvent/<str:pk>/', deleteEvent, name="deleteEvent"),
    path('deleteAnnouncement/<str:pk>/',
         deleteAnnouncement, name="deleteAnnouncement"),
    path('deleteBooking/<str:pk>/', deleteBooking, name="deleteBooking"),
    path('completeTask/<str:pk>/', completeTask, name="completeTask"),
]
