from django.contrib import admin
from .car import Car
from .models import Bid
from .models import SavedVehicle
from .models import VehicleFilter
from .models import State
from django.contrib.auth import get_user_model
User = get_user_model()

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff', 'drivers_license',
        )

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'drivers_license')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

class CarAdmin(admin.ModelAdmin):
    fieldsets = (
        ('General Information', {
            'fields': ('year', 'make', 'model', 'VIN', 'color', 'mileage', 'description')
        }),
        ('Images', {
            'fields': (
                'image_1', 'image_2', 'image_3', 'image_4', 'image_5',
                'image_6', 'image_7', 'image_8', 'image_9', 'image_10',
                'image_1_url', 'image_2_url', 'image_3_url', 'image_4_url', 'image_5_url',
                'image_6_url', 'image_7_url', 'image_8_url', 'image_9_url', 'image_10_url'
            )
        }),
        ('Vehicle Details', {
            'fields': ('engine', 'engine_displacement', 'cylinders', 'transmission', 'drive_type', 'vehicle_type', 'fuel_type', 'keys')
        }),
        ('Title and Classification', {
            'fields': ('title_classification', 'title_note')
        }),
        ('Damage Information - Driver Panels', {
            'fields': (
                'driver_headlight_damage', 'driver_fender_damage', 'driver_door_damage',
                'driver_rear_door_damage', 'driver_rocker_damage', 'driver_rear_wheel_arch_damage',
                'driver_rear_quarter_damage', 'driver_mirror_damage', 'driver_window_damage',
                'driver_rear_window_damage'
            )
        }),
        ('Damage Information - Passenger Panels', {
            'fields': (
                'passenger_headlight_damage', 'passenger_fender_damage', 'passenger_door_damage',
                'passenger_rear_door_damage', 'passenger_rocker_damage', 'passenger_rear_wheel_arch_damage',
                'passenger_rear_quarter_damage', 'passenger_mirror_damage', 'passenger_window_damage',
                'passenger_rear_window_damage'
            )
        }),
        ('Damage Information - Front Panels', {
            'fields': (
                'front_bumper_damage', 'radiator_support_damage', 'grille_damage', 'hood_damage'
            )
        }),
        ('Damage Information - Rear Panels', {
            'fields': (
                'roof_damage', 'deck_lid_damage', 'tailgate_damage', 'hatch_damage',
                'truck_bed_damage', 'rear_bumper_damage'
            )
        }),
        ('Damage Information - Glass', {
            'fields': (
                'windshield_damage', 'back_glass_damage', 'driver_tail_light_damage',
                'passenger_tail_light_damage'
            )
        }),
        ('Damage Information - Interior', {
            'fields': (
                'vehicle_starts', 'vehicle_drives', 'airbags_deployed'
            )
        }),
        ('Other Information', {
            'fields': ('active', 'condition', 'vehicle_zip', 'state', 'sale_date', 'auction', 'vehicle_auction_link', 'creator')
        }),
        ('Pricing', {
            'fields': ('starting_bid', 'current_bid', 'reserve_price', 'pure_sale', 'buy_it_now', 'buy_it_now_price')
        }),
    )

admin.site.register(Car, CarAdmin)
admin.site.register(Bid)
admin.site.register(SavedVehicle)
admin.site.register(VehicleFilter)
admin.site.register(User, UserAdmin)
admin.site.register(State)