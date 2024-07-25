from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import Guest, Employee


# Create your models here.
class Announcement(models.Model):
    content = models.TextField()
    sender = models.ForeignKey('accounts.Employee', null=True, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.sender)


class Event(models.Model):
    EVENT_TYPES = (
        ('Pelicula', 'Pelicula'),
        ('Teatro', 'Teatro'),
        ('Conferencia', 'Conferencia'),
        ('Concierto', 'Concierto'),
        ('Entretenimiento', 'Entretenimiento'),
        ('Musica', 'Musica'),
    )

    eventType = models.CharField(max_length=20, choices=EVENT_TYPES)
    location = models.CharField(max_length=100)
    startDate = models.DateField()
    endDate = models.DateField()
    explanation = models.TextField()

    def __str__(self):
        return str(self.eventType)


class EventAttendees(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    numberOfDependees = models.IntegerField(default=0)
    guest = models.ForeignKey('accounts.Guest',   null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.event) + " " + str(self.guest)


class Bills(models.Model):
    guest = models.ForeignKey('accounts.Guest',   null=True, on_delete=models.CASCADE)
    totalAmount = models.FloatField()
    summary = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.guest) + " " + str(self.summary) + " " + str(self.totalAmount)


class FoodMenu(models.Model):
    startDate = models.DateField()
    endDate = models.DateField()
    menuItems = models.TextField()

    def __str__(self):
        return str(self.menuItems) + " " + str(self.startDate)


class Report(models.Model):
    date = models.DateField(default=timezone.now)
    content = models.TextField()

    def __str__(self):
        return f"{self.content[:50]}... - {self.date}"


class Storage(models.Model):
    ITEM_TYPES = (
        ('Cocina', 'Cocina'),
        ('Limpieza', 'Limpieza'),
        ('Electronicos', 'Electronicos'),
        ('Lavanderia ', 'Lavanderia '),
        ('Otros', 'Otros'),
    )
    itemName = models.CharField(max_length=100)
    itemType = models.CharField(max_length=20, choices=ITEM_TYPES)
    quantitiy = models.IntegerField()

    def __str__(self):
        return str(self.itemName)
    


