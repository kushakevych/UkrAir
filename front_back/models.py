from django.db import models

import uuid

class User(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    passport_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

class Airport(models.Model):
    code_IATA = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    timezone = models.CharField(max_length=50)

class Aircraft(models.Model):
    model = models.CharField(max_length=50)

class SeatClass(models.Model):
    name = models.CharField(max_length=50)
    price_multiplier = models.DecimalField(max_digits=5, decimal_places=2)

class Seat(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    class_type = models.ForeignKey(SeatClass, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('available', 'Available'), ('reserved', 'Reserved'), ('unavailable', 'Unavailable')])

class Route(models.Model):
    flights_number = models.CharField(max_length=20, unique=True)
    departure = models.ForeignKey(Airport, related_name='departure', on_delete=models.CASCADE)
    arrival = models.ForeignKey(Airport, related_name='arrival', on_delete=models.CASCADE)
    duration_time = models.TimeField()
    days_of_week = models.CharField(max_length=20)
    is_popular = models.BooleanField(default=False)

class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()

class Booking(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('canceled', 'Canceled')])
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
