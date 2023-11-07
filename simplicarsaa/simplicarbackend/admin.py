from django.contrib import admin
from .car import Car
from .models import Bid
from .models import SavedVehicles

admin.site.register(Car)
admin.site.register(Bid)
admin.site.register(SavedVehicles)