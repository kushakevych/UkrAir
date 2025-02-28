from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Flight
from .forms import FlightSearchForm

def home_view(request):
    return render(request, "index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "Account.html", {"error": "Invalid username or password"})
    return render(request, "Account.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            return render(request, "Account.html", {"error": "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return render(request, "Account.html", {"error": "Username already exists"})

        user = User.objects.create_user(username=username, password=password)
        user.save()
        login(request, user)
        return redirect("home")

    return render(request, "Account.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


def search_flights(request):
    form = FlightSearchForm(request.GET)
    flights = Flight.objects.all()

    if form.is_valid():
        origin = form.cleaned_data.get('origin')
        destination = form.cleaned_data.get('destination')
        departure_date = form.cleaned_data.get('departure_date')

        if origin:
            flights = flights.filter(origin__icontains=origin)
        if destination:
            flights = flights.filter(destination__icontains=destination)
        if departure_date:
            flights = flights.filter(departure_time__date=departure_date)

    return render(request, 'search_results.html', {'form': form, 'flights': flights})

