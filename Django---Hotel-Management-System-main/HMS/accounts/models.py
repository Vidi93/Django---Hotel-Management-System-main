from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
# Create your models here.

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(unique=True)
    role = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

class Guest(models.Model):
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.custom_user.user.username

    def numOfBooking(self):
        return Booking.objects.filter(guest=self).count()

    def numOfDays(self):
        totalDay = 0
        bookings = Booking.objects.filter(guest=self)
        for b in bookings:
            day = b.endDate - b.startDate
            totalDay += int(day.days)
        return totalDay

    def numOfLastBookingDays(self):
        try:
            return int((Booking.objects.filter(guest=self).last().endDate - Booking.objects.filter(guest=self).last().startDate).days)
        except:
            return 0

    def currentRoom(self):
        booking = Booking.objects.filter(guest=self).last()
        return booking.roomNumber if booking else None


class Employee(models.Model):
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    salary = models.FloatField()

    def __str__(self):
        return self.custom_user.user.username

class Task(models.Model):
    employee = models.ForeignKey(Employee, null=True, on_delete=models.CASCADE)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return f"{self.employee} - {self.description}"
