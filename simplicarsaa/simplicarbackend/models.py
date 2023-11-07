from django.db import models
from django.contrib.auth.models import User
from .car import Car

# Create your models here.

class Bid(models.Model):
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_date = models.DateTimeField(auto_now=True)
    bid_vehicle = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f'Bid {self.id} on {self.bid_vehicle}'

    def get_bids(self):
        return Bid.objects.filter(bid_vehicle=self)
    
    def __str__(self):
        return f'{self.year} {self.make} {self.model} - {self.VIN}'

class SavedVehicles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    saved_vehicle = models.ForeignKey(Car, on_delete=models.CASCADE)
