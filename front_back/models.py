from django.contrib.auth.models import AbstractUser
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Хешує пароль
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперкористувач повинен мати is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперкористувач повинен мати is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    passport_number = models.CharField(max_length=20)
    is_staff = models.BooleanField(default=False)  # Додаємо поле для доступу до адмінки

    objects = UserManager()
    USERNAME_FIELD = 'email'  # Вказуємо, що email — це логін
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

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

class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
