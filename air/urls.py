from django.urls import path
from .views import login_view, register_view, logout_view, book_flight, account_view, profile_view, place_view,  home_view
from .views import get_flights, get_aircraft_seats, book_seat, get_services, search_flights, purchase_seat, cancel_booking
from django.shortcuts import render
from .views import index_view


urlpatterns = [
    path('', index_view, name='index'),
    path('', lambda request: render(request, 'index.html'), name='index'),
    path('account/', account_view, name='account'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path("logout/", logout_view, name="logout"),
    path("book/<int:flight_id>/", book_flight, name="book_flight"),
    path('kabinet/', profile_view, name='kabinet'),
    path("place/", place_view, name="place"),
    path("api/flights/", get_flights, name="get_flights"),
    path("api/seats/<int:flight_id>/", get_aircraft_seats, name="get_aircraft_seats"),
    path("api/book_seat/", book_seat, name="book_seat"),
    path("api/services/", get_services, name="get_services"),
    path("api/purchase/", purchase_seat, name="purchase_seat"),
    path("api/cancel/", cancel_booking, name="cancel_booking"),
]
