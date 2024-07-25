from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User, Group
# Create your models here.

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(unique=True)
    role = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Guest(models.Model):
    custom_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.custom_user.user.username

    def numOfBooking(self):
        return self.booking_set.count()

    def numOfDays(self):
        totalDay = 0
        bookings = self.booking_set.all()
        for b in bookings:
            day = b.endDate - b.startDate
            totalDay += day.days
        return totalDay

    def numOfLastBookingDays(self):
        last_booking = self.booking_set.last()
        if last_booking:
            return (last_booking.endDate - last_booking.startDate).days
        return 0

    def currentRoom(self):
        last_booking = self.booking_set.last()
        return last_booking.roomNumber if last_booking else None


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
