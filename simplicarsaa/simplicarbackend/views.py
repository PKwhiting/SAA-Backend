import json
from django.shortcuts import render

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
from .serializers import CarSerializer

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
   car_vin = data.get('vehicle_vin')
   car = Car.objects.get(VIN=car_vin)
   print(car.current_bid)
   car.current_bid = data.get('bid')
   print(car.current_bid)
   car.save()
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
            print("LOGIN")
            if User.objects.filter(username=username).exists():
                user = authenticate(request, username=username, password=password)
               
                if user is not None:
                    login(request, user)
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False, 'message': 'Invalid username or password'})
            else:
                return JsonResponse({'success': False, 'message': 'Username does not exist'})
        else:  # User registration
            if not User.objects.filter(username=username).exists():  # Check if username does not exist
                try:
                    user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
                    user.save()
                    return JsonResponse({'success': True})
                except Exception as e:
                    return JsonResponse({'success': False, 'message': str(e)})
            else:
                return JsonResponse({'success': False, 'message': 'Username already exists'})

    return JsonResponse({'success': False, 'message': 'Invalid request'})