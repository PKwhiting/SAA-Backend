from django.db import models

# Create your models here.
#define a car model
class Car(models.Model):
    year = models.IntegerField()
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    VIN = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    mileage = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=1000, blank=True)
    image = models.ImageField(upload_to='cars', blank=True)
    active = models.BooleanField(default=True)
    condition = models.CharField(max_length=100, blank=True)
    lot_location = models.CharField(max_length=100, blank=True)
    sale_info = models.TextField()

    def __str__(self):
        return self.make + ' ' + self.model + ' ' + str(self.year)