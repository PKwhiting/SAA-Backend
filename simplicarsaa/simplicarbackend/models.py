from django.db import models
from django.contrib.auth.models import User
# from .models import Bid

# Create your models here.

class Bid(models.Model):
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_date = models.DateTimeField(auto_now=True)
    bid_vehicle = models.ForeignKey('Car', on_delete=models.CASCADE)

    def __str__(self):
        return f'Bid {self.id} on {self.bid_vehicle}'
    
class Car(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    year = models.IntegerField()
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    VIN = models.CharField(max_length=100)
    title_code = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=100)
    engine = models.CharField(max_length=100, blank=True)
    engine_displacement = models.FloatField(blank=True, null=True)
    cylinders = models.IntegerField(blank=True)
    transmission = models.CharField(max_length=100, blank=True)
    drive_type = models.CharField(max_length=100, blank=True)
    vehicle_type = models.CharField(max_length=100, blank=True)
    fuel_type = models.CharField(max_length=100, blank=True)
    keys = models.IntegerField(blank=True, null=True)
    mileage = models.IntegerField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0.0)
    reserve_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    active = models.BooleanField(default=True)
    condition = models.CharField(max_length=100, blank=True)
    vehicle_location = models.TextField()
    sale_date = models.DateTimeField()
    last_updated = models.DateTimeField(auto_now=True)
    image_1 = models.ImageField(upload_to='cars', blank=True)
    image_2 = models.ImageField(upload_to='cars', blank=True)
    image_3 = models.ImageField(upload_to='cars', blank=True)
    image_4 = models.ImageField(upload_to='cars', blank=True)
    image_5 = models.ImageField(upload_to='cars', blank=True)
    image_6 = models.ImageField(upload_to='cars', blank=True)
    image_7 = models.ImageField(upload_to='cars', blank=True)
    image_8 = models.ImageField(upload_to='cars', blank=True)
    image_9 = models.ImageField(upload_to='cars', blank=True)
    image_10 = models.ImageField(upload_to='cars', blank=True)

    # undamages/usable parts
    vehicle_starts = models.BooleanField(default=False)
    vehicle_drives = models.BooleanField(default=False)
    bumper_damage = models.BooleanField(default=False)
    driver_headlight_damage = models.BooleanField(default=False)
    passenger_headlight_damage = models.BooleanField(default=False)
    hood_damage = models.BooleanField(default=False)
    roof_damage = models.BooleanField(default=False)
    driver_fender_damage = models.BooleanField(default=False)
    passenger_fender_damage = models.BooleanField(default=False)
    driver_door_damage = models.BooleanField(default=False)
    passenger_door_damage = models.BooleanField(default=False)
    driver_rear_door_damage = models.BooleanField(default=False)
    passenger_rear_door_damage = models.BooleanField(default=False)
    driver_rocker_damage = models.BooleanField(default=False)
    passenger_rocker_damage = models.BooleanField(default=False)
    driver_rear_wheel_arch_damage = models.BooleanField(default=False)
    passenger_rear_wheel_arch_damage = models.BooleanField(default=False)
    driver_rear_quarter_damage = models.BooleanField(default=False)
    passenger_rear_quarter_damage = models.BooleanField(default=False)
    trunk_damage = models.BooleanField(default=False)
    rear_bumper_damage = models.BooleanField(default=False)
    driver_tail_light_damage = models.BooleanField(default=False)
    passenger_tail_light_damage = models.BooleanField(default=False)
    driver_mirror_damage = models.BooleanField(default=False)
    passenger_mirror_damage = models.BooleanField(default=False)
    windshield_damage = models.BooleanField(default=False)
    driver_window_damage = models.BooleanField(default=False)
    passenger_window_damage = models.BooleanField(default=False)
    driver_rear_window_damage = models.BooleanField(default=False)
    passenger_rear_window_damage = models.BooleanField(default=False)
    back_glass_damage = models.BooleanField(default=False)
    truck_bed_damage = models.BooleanField(default=False)




    def get_bids(self):
        return Bid.objects.filter(bid_vehicle=self)
    
    def __str__(self):
        return f'{self.year} {self.make} {self.model} - {self.VIN}'

