from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.area}, {self.city}"

class Turf(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    sport_type = models.CharField(max_length=50)
    price_per_hour = models.IntegerField()

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    turf = models.ForeignKey(Turf, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.CharField(max_length=50)
    booked_on = models.DateTimeField(auto_now_add=True)
