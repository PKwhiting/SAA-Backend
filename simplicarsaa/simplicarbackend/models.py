from django.db import models
from .user import User
from .car import Car
from .state import State
from django.contrib.auth import get_user_model
User = get_user_model()
 

# Create your models here.å

class Bid(models.Model):
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_date = models.DateTimeField(auto_now=True)
    bid_vehicle = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f'Bid {self.id} on {self.bid_vehicle}'

    def get_bids(self):
        return Bid.objects.filter(bid_vehicle=self)

class SavedVehicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    saved_vehicle = models.ForeignKey(Car, on_delete=models.CASCADE)

class VehicleFilter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    make = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    start_year = models.IntegerField(blank=True, null=True)
    end_year = models.IntegerField(blank=True, null=True)
    vehicle_starts = models.BooleanField(default=False)
    damageFields = models.TextField(blank=True, null=True)
    filter_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.filter_name


