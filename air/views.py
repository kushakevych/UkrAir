from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import FlightSearchForm, BookingForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Flight, Seat, Booking, Service
from datetime import datetime



def index_view(request):
    return render(request, "index.html", {"user": request.user})

def home_view(request):
    return render(request, "index.html")

def account_view(request):
    return render(request, "Account.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "Account.html", {"error": "Невірний логін або пароль"})

    return render(request, "Account.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            return render(request, "Account.html", {"error": "Користувач вже існує"})

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect("index")

    return render(request, "Account.html")

@login_required
def profile_view(request):
    return render(request, "profile.html", {"user": request.user})

def place_view(request):
    return render(request, "place.html", {"user": request.user})

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

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
    date = request.GET.get("date")

    if not departure or not arrival or not date:
        return JsonResponse({"error": "Недостатньо даних для пошуку"}, status=400)

    try:
        parsed_date = datetime.strptime(date, "%d %B %Y").strftime("%Y-%m-%d")
    except ValueError:
        return JsonResponse({"error": "Неправильний формат дати"}, status=400)

    flights = Flight.objects.filter(
        route__departure__city=departure,
        route__arrival__city=arrival,
        departure_time__date=parsed_date
    ).values("id", "aircraft", "departure_time")

    return JsonResponse(list(flights), safe=False)


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
            departure_date=parse_date(date)
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