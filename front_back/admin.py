from django.contrib import admin
from .models import User, Airport, Aircraft, SeatClass, Seat, Route, Flight, Booking

@admin.register(User, Airport, Aircraft, SeatClass, Seat, Route, Flight, Booking)
class DefaultAdmin(admin.ModelAdmin):
    pass