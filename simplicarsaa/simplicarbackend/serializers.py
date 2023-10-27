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
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ['id', 'make', 'model', 'year', 'image_url']

    def get_image_url(self, car):
        request = self.context.get('request')
        return request.build_absolute_uri(car.image.url)