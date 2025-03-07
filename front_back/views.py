from email.utils import parsedate
from django.contrib.auth import authenticate, login, logout
from front_back.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BookingForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Flight, Route, Seat, Booking, SeatClass, Service
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password

def time_to_timedelta(t):
    return timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond)

def index_view(request):
    popular_routes = Route.objects.filter(is_popular=True)
    print(popular_routes)
    return render(request, "index.html", {"user": request.user, "popular_routes": popular_routes})

def home_view(request):
    return render(request, "index.html")

def account_view(request):
    return render(request, "Account.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        
        if not email or not password:
            return render(request, "Account.html", {"error": "Заповніть усі поля"})
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "Account.html", {"error": "Невірний email або пароль"})
    
    return render(request, "Account.html")

def register_view(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        passport_number = request.POST["passport_number"]

        if User.objects.filter(email=email).exists():
            return render(request, "Account.html", {"error": "Користувач вже існує"})

        user = User.objects.create(first_name=first_name, last_name=last_name, passport_number=passport_number, email=email, password=make_password(password))
        login(request, user)
        return redirect("index")

    return render(request, "Account.html")

@login_required
def profile_view(request):
    # Отримуємо поточного користувача
    user = request.user
    
    # Отримуємо всі бронювання зі статусом 'confirmed' для цього користувача
    bookings = Booking.objects.filter(user=user, status='confirmed')
    
    # Створюємо список квитків із необхідною інформацією
    tickets = []
    for booking in bookings:
        flight = booking.flight
        seat = booking.seat
        tickets.append({
            'flight_date': flight.departure_time.strftime('%d %B, %A'),
            'departure_time': flight.departure_time.strftime('%H:%M'),
            'arrival_time': flight.arrival_time.strftime('%H:%M'),
            'departure_city': flight.departure_city,
            'arrival_city': flight.arrival_city,
            'seat_number': seat.seat_number,
            # Тут можна додати тривалість рейсу, якщо вона розраховується
        })
    
    # Передаємо дані в контекст для шаблону
    context = {
        'user': user,
        'tickets': tickets,
    }
    return render(request, 'profile.html', context)

def place_view(request):
    return render(request, "place.html", {"user": request.user})

@login_required
def logout_view(request):
    logout(request)
    return redirect("index")

@login_required
def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.is_paid = False
            booking.is_cancelled = False
            booking.save()
            return redirect('payment', booking_id=booking.id)
    else:
        form = BookingForm(initial={'flight': flight})
    return render(request, 'booking.html', {'form': form, 'flight': flight})


def get_flights(request):
    departure = request.GET.get("departure")
    arrival = request.GET.get("arrival")
    date_str = request.GET.get("date")
    print(date_str)

    if not departure or not arrival or not date_str:
        return render(request, 'index.html', {'error': 'Недостатньо даних для пошуку'})

    try:
        parsed_date = datetime.strptime(date_str, "%d-%m-%Y").date()
    except ValueError:
        return render(request, 'index.html', {'error': 'Неправильний формат дати'})

    flights = Flight.objects.filter(
        route__departure__city=departure,
        route__arrival__city=arrival,
        departure_time__date=parsed_date
    )

    flight_data = []
    for flight in flights:
        print("1")
        route = flight.route
        aircraft = flight.aircraft
        departure_time = flight.departure_time

        # Розрахунок часу прибуття
        duration = route.duration_time
        duration_td = time_to_timedelta(duration)
        arrival_time = departure_time + duration_td

        # Отримання класів сидінь та доступних місць
        seat_classes = SeatClass.objects.filter(seat__aircraft=aircraft).distinct()
        classes_data = []
        for seat_class in seat_classes:
            available_seats_count = Seat.objects.filter(
                aircraft=aircraft,
                class_type=seat_class,
                status='available'
            ).count()
            price = seat_class.price_multiplier  # Припускаємо, що це ціна
            classes_data.append({
                "name": seat_class.name,
                "available_seats": available_seats_count,
                "price": price
            })

        flight_data.append({
            "flight_id": flight.id,
            "flight_number": route.flights_number,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
            "departure_city": route.departure.city,
            "arrival_city": route.arrival.city,
            "duration": duration,
            "classes": classes_data
        })

    context = {
        "flights": flight_data,
        "departure": departure,
        "arrival": arrival,
        "date": parsed_date
    }

    return render(request, "booking.html", context)


def get_aircraft_seats(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    seats = Seat.objects.filter(aircraft=flight.aircraft)

    data = [{"seat_number": seat.seat_number, "class": seat.class_type.name, "status": seat.status} for seat in seats]
    return JsonResponse(data, safe=False)

@csrf_exempt
def book_seat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        flight_id = data.get("flight_id")
        seat_number = data.get("seat_number")
        user_id = data.get("user_id")

        flight = get_object_or_404(Flight, id=flight_id)
        seat = get_object_or_404(Seat, aircraft=flight.aircraft, seat_number=seat_number)

        if seat.status != "available":
            return JsonResponse({"error": "Місце вже зайняте"}, status=400)

        booking = Booking.objects.create(flight=flight, seat=seat, user_id=user_id, status="pending")
        seat.status = "reserved"
        seat.save()

        return JsonResponse({"message": "Місце заброньовано", "booking_id": booking.id})

def get_services(request):
    services = Service.objects.all()
    data = [{"id": service.id, "name": service.name, "price": float(service.price)} for service in services]
    return JsonResponse(data, safe=False)

@csrf_exempt
def purchase_seat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        booking_id = data.get("booking_id")

        booking = get_object_or_404(Booking, id=booking_id)

        if booking.status == "confirmed":
            return JsonResponse({"error": "Місце вже оплачено"}, status=400)

        booking.status = "confirmed"
        booking.save()

        return JsonResponse({"message": "Квиток оплачено"})


@csrf_exempt
def cancel_booking(request):
    if request.method == "POST":
        data = json.loads(request.body)
        booking_id = data.get("booking_id")

        booking = get_object_or_404(Booking, id=booking_id)

        if booking.status == "canceled":
            return JsonResponse({"error": "Квиток вже скасовано"}, status=400)

        booking.status = "canceled"
        booking.seat.status = "available"
        booking.seat.save()
        booking.save()

        return JsonResponse({"message": "Квиток скасовано"})

@csrf_exempt
def search_flights(request):
    if request.method == "GET":
        from_city = request.GET.get("from", "").strip()
        to_city = request.GET.get("to", "").strip()
        date = request.GET.get("date", "").strip()

        if not from_city or not to_city or not date:
            return JsonResponse({"error": "Всі параметри обов’язкові"}, status=400)

        flights = Flight.objects.filter(
            from_city__iexact=from_city,
            to_city__iexact=to_city,
            departure_date=parsedate(date)
        )

        flights_data = [
            {
                "from": flight.from_city,
                "to": flight.to_city,
                "departure_time": flight.departure_time.strftime("%H:%M"),
                "price": flight.price,
            }
            for flight in flights
        ]

        return JsonResponse(flights_data, safe=False)

    return JsonResponse({"error": "Метод не дозволено"}, status=405)