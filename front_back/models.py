from django.db import models

class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.flight_number}: {self.origin} → {self.destination}"
