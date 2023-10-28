from django.db import models

# Create your models here.
#define a car model
class Car(models.Model):
    year = models.IntegerField()
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    VIN = models.CharField(max_length=100)
    title_code = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=100)
    engine = models.CharField(max_length=100, blank=True)
    cylinders = models.IntegerField(blank=True)
    transmission = models.CharField(max_length=100, blank=True)
    drive_type = models.CharField(max_length=100, blank=True)
    vehicle_type = models.CharField(max_length=100, blank=True)
    fuel_type = models.CharField(max_length=100, blank=True)
    keys = models.IntegerField(blank=True)
    mileage = models.IntegerField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0.0)
    reserve_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    description = models.TextField(max_length=1000, blank=True)
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


    def __str__(self):
        return self.make + ' ' + self.model + ' ' + str(self.year)