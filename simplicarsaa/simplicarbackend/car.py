from django.db import models
from django.contrib.auth import get_user_model
from .state import State

User = get_user_model()

# Choices for fields
AUCTION_CHOICES = [
    ('SAA', 'SAA'),
    ('COPART', 'COPART'),
    ('IAA', 'IAA'),
]

VEHICLE_CATEGORY_CHOICES = [
    ('AUTOMOBILE', 'AUTOMOBILE'),
    ('MOTORCYCLE', 'MOTORCYCLE'),
    ('RV', 'RV'),
    ('BOAT', 'BOAT'),
    ('TRAILER', 'TRAILER'),
    ('OTHER', 'OTHER'),
]

ODOMETER_BRAND_CHOICES = [
    ('ACTUAL', 'ACTUAL'),
    ('EXEMPT', 'EXEMPT'),
    ('NOT ACTUAL', 'NOT ACTUAL'),
    ('INOPERABLE', 'INOPERABLE'),
    ('OTHER', 'OTHER'),
]

TITLE_CHOICES = [
    ('CLEAN', 'CLEAN'),
    ('SALVAGE', 'SALVAGE'),
    ('REBUILT', 'REBUILT'),
    ('EXPORT ONLY', 'EXPORT ONLY'),
    ('PARTS ONLY', 'PARTS ONLY'),
    ('OTHER', 'OTHER'),
]

class Car(models.Model):
    # Vehicle details
    year = models.IntegerField()
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    VIN = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    engine = models.CharField(max_length=100, blank=True)
    engine_displacement = models.CharField(max_length=100, blank=True, default=0.0)
    cylinders = models.IntegerField(blank=True)
    transmission = models.CharField(max_length=100, blank=True)
    drive_type = models.CharField(max_length=100, blank=True)

    #SUV/Truck/Sedan
    vehicle_type = models.CharField(max_length=100, blank=True)


    fuel_type = models.CharField(max_length=100, blank=True)
    keys = models.IntegerField(blank=True, null=True)
    mileage = models.IntegerField()
    odometer_brand = models.CharField(max_length=100, blank=True, choices=ODOMETER_BRAND_CHOICES)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0.0)
    reserve_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    pure_sale = models.BooleanField(default=False)
    buy_it_now = models.BooleanField(default=False)
    buy_it_now_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    active = models.BooleanField(default=True)
    condition = models.CharField(max_length=100, blank=True)
    vehicle_zip = models.CharField(max_length=10, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, blank=True, null=True)
    sale_date = models.DateTimeField()
    last_updated = models.DateTimeField(auto_now=True)

    # Auction details
    auction = models.CharField(max_length=100, choices=AUCTION_CHOICES, default='SAA')
    vehicle_auction_link = models.CharField(max_length=100, blank=True, null=True)

    # Title details
    title_classification = models.CharField(max_length=100, choices=TITLE_CHOICES, default='CLEAN')
    title_note = models.CharField(max_length=100, blank=True)
    

    # Creator details
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # Images
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
    image_1_url = models.URLField(blank=True, null=True)
    image_2_url = models.URLField(blank=True, null=True)
    image_3_url = models.URLField(blank=True, null=True)
    image_4_url = models.URLField(blank=True, null=True)
    image_5_url = models.URLField(blank=True, null=True)
    image_6_url = models.URLField(blank=True, null=True)
    image_7_url = models.URLField(blank=True, null=True)
    image_8_url = models.URLField(blank=True, null=True)
    image_9_url = models.URLField(blank=True, null=True)
    image_10_url = models.URLField(blank=True, null=True)

    # Undamages/usable parts
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

    def __str__(self):
        return f'{self.year} {self.make} {self.model} - {self.VIN}'