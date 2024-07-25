from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['roomNumber', 'startDate', 'endDate']
        widgets = {
            'startDate': forms.DateInput(attrs={'type': 'date'}),
            'endDate': forms.DateInput(attrs={'type': 'date'}),
        }