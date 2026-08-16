from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('turf', 'user', 'date', 'start_time', 'end_time', 'status', 'total_price')
    list_filter = ('status', 'date', 'turf__city')
    search_fields = ('turf__name', 'user__username')
    autocomplete_fields = ('turf', 'user')
    date_hierarchy = 'date'
