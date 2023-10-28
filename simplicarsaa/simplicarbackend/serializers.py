from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Car

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

    class Meta:
        model = Car
        fields = ['id', 'year', 'make', 'model', 'VIN','title_code', 'color', 'engine', 'cylinders', 'transmission', 'drive_type', 'vehicle_type', 'fuel_type', 'keys', 'mileage', 'starting_bid', 'reserve_price', 'description', 'active', 'condition', 'vehicle_location', 'sale_date', 'last_updated', 'images']

    def get_images(self, car):
        request = self.context.get('request')
        images = []
        for i in range(1, 11):
            image_field = getattr(car, f'image_{i}')
            if image_field:
                images.append(request.build_absolute_uri(image_field.url))
        return images