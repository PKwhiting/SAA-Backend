from django.contrib import admin
from .car import Car
from .models import Bid
from .models import SavedVehicle
from .models import VehicleFilter

admin.site.register(Car)
admin.site.register(Bid)
admin.site.register(SavedVehicle)
admin.site.register(VehicleFilter)