from django import forms
from .models import Booking
from .models import Room

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['roomNumber', 'startDate', 'endDate']
        widgets = {
            'startDate': forms.DateInput(attrs={'type': 'date'}),
            'endDate': forms.DateInput(attrs={'type': 'date'}),
        }

class RoomEditForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['capacity', 'numberOfBeds', 'roomType', 'price', 'statusStartDate', 'statusEndDate']