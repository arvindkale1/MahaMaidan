from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('turf/<int:turf_pk>/book/', views.create_booking, name='create_booking'),
    path('mine/', views.MyBookingsView.as_view(), name='my_bookings'),
    path('<int:pk>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('turf/<int:turf_pk>/all/', views.TurfBookingsView.as_view(), name='turf_bookings'),
]
