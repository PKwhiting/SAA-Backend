from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import Car, Bid
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class CarSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    highest_bid = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ['id', 'year', 'make', 'model', 'VIN', 'color', 'engine', 'engine_displacement', 'cylinders', 'transmission', 'drive_type', 'vehicle_type', 'fuel_type', 'keys', 'mileage',
                  'odometer_brand', 'starting_bid', 'current_bid', 'reserve_price', 'pure_sale', 'buy_it_now_price', 'description', 'active', 'condition', 'vehicle_zip', 'state', 'sale_date', 'last_updated',
                  'auction', 'vehicle_auction_link', 'title_code', 'title_classification', 'creator', 'images', 'highest_bid',
                  'vehicle_starts', 'vehicle_drives', 'bumper_damage', 'driver_headlight_damage', 'passenger_headlight_damage', 'hood_damage', 'roof_damage',
                  'driver_fender_damage', 'passenger_fender_damage', 'driver_door_damage', 'passenger_door_damage', 'driver_rear_door_damage', 'passenger_rear_door_damage',
                  'driver_rocker_damage', 'passenger_rocker_damage', 'driver_rear_wheel_arch_damage', 'passenger_rear_wheel_arch_damage', 'driver_rear_quarter_damage',
                  'passenger_rear_quarter_damage', 'trunk_damage', 'rear_bumper_damage', 'driver_tail_light_damage', 'passenger_tail_light_damage',
                  'driver_mirror_damage', 'passenger_mirror_damage', 'windshield_damage', 'driver_window_damage', 'passenger_window_damage', 'driver_rear_window_damage',
                  'passenger_rear_window_damage', 'back_glass_damage', 'truck_bed_damage']

    def get_images(self, car):
        request = self.context.get('request')
        images = []
        for i in range(1, 11):
            image_field = getattr(car, f'image_{i}')
            image_field_url = getattr(car, f'image_{i}_url')
            if image_field:
                images.append(request.build_absolute_uri(image_field.url))
            elif image_field_url:
                images.append(image_field_url)
        return images

    def get_highest_bid(self, car):
        highest_bid = Bid.objects.filter(
            bid_vehicle=car).order_by('-bid_amount').first()
        if highest_bid:
            return highest_bid.bid_amount
        else:
            return None
