import json
import datetime
import base64
import os
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from simplicarbackend.serializers import UserSerializer, GroupSerializer
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import get_token
from django.views.decorators.csrf import requires_csrf_token
from rest_framework.decorators import api_view
from .models import Car
from .models import Bid
from .serializers import CarSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings

def index(request):
    return render(request, 'index.html')

def get_csrf_token(request):
    response = JsonResponse({'csrfToken': get_token(request)})
    response.set_cookie('csrftoken', get_token(request), httponly=True, samesite='None', secure=True)
    return response

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

def ActiveVehicles(request):
    cars = Car.objects.filter(active=True)
    serializer = CarSerializer(cars, many=True, context={'request': request})
    return JsonResponse({'cars': serializer.data})


# rewrite the car_detail view to get the id from the query parameter
def car_detail(request):
   car_id = request.GET.get('id')
   car = Car.objects.get(pk=car_id)
   serializer = CarSerializer(car, context={'request': request})
   return JsonResponse({'car': serializer.data})

@requires_csrf_token
@api_view(['POST'])
def update_current_bid(request):
   data = json.loads(request.body)
   userID = data.get('userID')
   car = Car.objects.get(VIN=data.get('vehicle_vin'))
   user = User.objects.get(pk=userID)
   bid = Bid.objects.create(bid_amount=data.get('bid'), bidder=user, bid_vehicle=car)
   bid.save()
   car.current_bid = data.get('bid')
   serializer = CarSerializer(car, context={'request': request})
   return JsonResponse({'car': serializer.data})


@requires_csrf_token
@api_view(['POST'])
def login_or_register(request):
    csrf_token = get_token(request)  # Obtain the CSRF token
    response = JsonResponse({'success': False, 'message': 'Invalid request'})
    response.set_cookie('csrftoken', csrf_token)  # Set the CSRF token in the response cookie
    response['X-Frame-Options'] = 'DENY'  # Set the X-Frame-Options header
    if request.method == 'POST':
        data = json.loads(request.body)  # Parse JSON request data
        username = data.get('username')
        password = data.get('password')
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        email = data.get('email')
        is_login = data.get('isLogin')

        if is_login:  # User login
            if User.objects.filter(username=username).exists():
                user = authenticate(request, username=username, password=password)
               
                if user is not None:
                    login(request, user)
                    return JsonResponse({'success': True, 'userID': user.id})
                else:
                    return JsonResponse({'success': False, 'message': 'Invalid username or password'})
            else:
                return JsonResponse({'success': False, 'message': 'Username does not exist'})
        else:  # User registration
            if not User.objects.filter(username=username).exists():  # Check if username does not exist
                try:
                    user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
                    user.save()
                    return JsonResponse({'success': True, 'userID': user.id})
                except Exception as e:
                    return JsonResponse({'success': False, 'message': str(e)})
            else:
                return JsonResponse({'success': False, 'message': 'Username already exists'})

    return JsonResponse({'success': False, 'message': 'Invalid request'})

@requires_csrf_token
@api_view(['POST'])
def add_vehicle(request):
    if request.method == 'POST':
        year = request.data.get('year')
        make = request.data.get('make')
        model = request.data.get('model')
        VIN =request.data.get('vin')
        title_code = request.data.get('titleStatus')
        color = request.data.get('color')
        engine = request.data.get('engineType')
        engine_displacement = request.data.get('displacement')
        cylinders = request.data.get('cylinders')
        transmission = request.data.get('transmission')
        drive_type = request.data.get('drive')
        vehicle_type = request.data.get('vehicleType')
        fuel_type = request.data.get('fuel')
        keys = request.data.get('numKeys')
        mileage = request.data.get('odometer')
        starting_bid = 0
        current_bid = 0
        reserve_price = float(request.data.get('reservePrice', 0)) if request.data.get('reservePrice', '') != '' else 0
        description = request.data.get('description')
        active = False
        condition = 'Good'
        vehicle_location = request.data.get('location')
        saleDate = (datetime.date.today() + datetime.timedelta((5 - datetime.date.today().weekday()) % 7)).strftime('%Y-%m-%d') + 'T12:00:00Z'
        user = User.objects.get(pk=request.data.get('userID'))

        car = Car(
            year=year,
            make=make,
            model=model,
            VIN=VIN,
            title_code=title_code,
            color=color,
            engine=engine,
            engine_displacement=engine_displacement,
            cylinders=cylinders,
            transmission=transmission,
            drive_type=drive_type,
            vehicle_type=vehicle_type,
            fuel_type=fuel_type,
            keys=keys,
            mileage=mileage,
            starting_bid=starting_bid,
            current_bid=current_bid,
            reserve_price=reserve_price,
            description=description,
            active=active,
            condition=condition,
            vehicle_location=vehicle_location,
            sale_date=saleDate,
            creator=user
        )
        images = request.FILES.getlist('images')
        i = 0
        for i, image in enumerate(images):
            setattr(car, f"image_{i+1}", image)
        car.save()
        return JsonResponse({'success': True})
    else:
        return HttpResponseBadRequest('Invalid request method')