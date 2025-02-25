from django.urls import path
from .views import login_view, register_view, logout_view
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
]
