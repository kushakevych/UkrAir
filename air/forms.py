from django import forms
from .models import Booking

class FlightSearchForm(forms.Form):
    origin = forms.CharField(label="Звідки", max_length=100, required=False)
    destination = forms.CharField(label="Куди", max_length=100, required=False)
    departure_date = forms.DateField(label="Дата вильоту", required=False, widget=forms.SelectDateWidget)

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['flight', 'seat']
