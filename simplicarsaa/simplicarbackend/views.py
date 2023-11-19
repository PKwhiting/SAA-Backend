import json
import datetime
import base64
import os

from django.core.files.base import ContentFile
from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse

from django.contrib.auth.models import User, Group
# from .user import User
from rest_framework import viewsets
from rest_framework import permissions
from simplicarbackend.serializers import UserSerializer, GroupSerializer
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import get_token
from django.views.decorators.csrf import requires_csrf_token
from rest_framework.decorators import api_view
from .models import Car
from .models import Bid
from .models import SavedVehicle
from .models import VehicleFilter
from .serializers import CarSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings
from datetime import date, timedelta
from django.core.paginator import Paginator
from django.core.mail import send_mail

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

@requires_csrf_token
@api_view(['POST'])
def ActiveVehicles(request):
    cars = Car.objects.filter(active=True)
    data = json.loads(request.body)
    make = data.get('makes')
    model = data.get('models')
    yearsStart = data['years'].get('start')
    sold = data.get('sold')
    yearsEnd = data['years'].get('end')
    if make:
        cars = cars.filter(make__icontains=make)
    if model:
        cars = cars.filter(model__icontains=model)
    if yearsStart and yearsEnd:
        start_year, end_year = int(yearsStart), int(yearsEnd)
        cars = cars.filter(year__gte=start_year, year__lte=end_year)
    elif yearsStart:
        start_year = int(yearsStart)
        cars = cars.filter(year__gte=start_year)
    elif yearsEnd:
        end_year = int(yearsEnd)
        cars = cars.filter(year__lte=end_year)

    today = date.today()
    if sold:
        cars = cars.filter(sale_date__lte=today)
    else:
        cars = cars.filter(sale_date__gte=today)
    
    
    paginator = Paginator(cars, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    serializer = CarSerializer(page_obj, many=True, context={'request': request})
    return JsonResponse({
        'cars': serializer.data,
        'num_pages': paginator.num_pages,
    })



def saved_vehicles(request, user_id):
    user = User.objects.get(pk=user_id)
    saved_cars = SavedVehicle.objects.filter(user=user).select_related('saved_vehicle')
    cars = [saved_vehicle.saved_vehicle for saved_vehicle in saved_cars]
    serializer = CarSerializer(cars, many=True, context={'request': request})
    return JsonResponse({'saved_cars': serializer.data})
    
@requires_csrf_token
@api_view(['POST'])
def add_saved_vehicle(request, user_id):
    data = json.loads(request.body)
    user = User.objects.get(pk=user_id)
    car = Car.objects.get(id=data.get('carID'))
    saved_vehicle, created = SavedVehicle.objects.get_or_create(user=user, saved_vehicle=car)
    if created:
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Vehicle already saved'})
    
@requires_csrf_token
@api_view(['POST'])
def remove_saved_vehicle(request, user_id):
    data = json.loads(request.body)
    user = User.objects.get(pk=user_id)
    car = Car.objects.get(id=data.get('carID'))
    saved_vehicle = SavedVehicle.objects.filter(user=user, saved_vehicle=car).first()
    if saved_vehicle:
        saved_vehicle.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Vehicle not found'})


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
                    return JsonResponse({'success': True, 'userID': user.id, 'isStaff': user.is_staff})
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
        year = request.POST.get('year')
        make = request.POST.get('make')
        model = request.POST.get('model')
        VIN = request.POST.get('vin')
        title_code = request.POST.get('titleStatus')
        color = request.POST.get('color')
        engine = request.POST.get('engineType')
        engine_displacement = 0 if request.POST.get('displacement') == '' else request.POST.get('displacement')
        cylinders = 0 if request.POST.get('cylinders') == '' else request.POST.get('cylinders')
        transmission = request.POST.get('transmission')
        drive_type = request.POST.get('drive')
        vehicle_type = request.POST.get('vehicleType')
        fuel_type = request.POST.get('fuel')
        keys = request.POST.get('numKeys')
        mileage = request.POST.get('odometer')
        starting_bid = 0
        current_bid = 0
        reserve_price = float(request.POST.get('reservePrice', 0)) if request.POST.get('reservePrice', '') != '' else 0
        description = request.POST.get('description')
        active = False
        condition = 'Good'
        vehicle_location = request.POST.get('location')
        sale_date = (date.today() + timedelta((5 - date.today().weekday()) % 7)).strftime('%Y-%m-%d') + 'T12:00:00Z'
        user = User.objects.get(pk=request.POST.get('userID'))
        vehicle_starts=json.loads(request.POST.get('vehicleRuns', False))
        vehicle_drives=json.loads(request.POST.get('vehicleDrives', False))
        bumper_damage=json.loads(request.POST.get('bumper_damage', False))
        driver_headlight_damage=json.loads(request.POST.get('driver_headlight_damage', False))
        passenger_headlight_damage=json.loads(request.POST.get('passenger_headlight_damage', False))
        hood_damage=json.loads(request.POST.get('hood_damage', False))
        roof_damage=json.loads(request.POST.get('roof_damage', False))
        driver_fender_damage=json.loads(request.POST.get('driver_fender_damage', False))
        passenger_fender_damage=json.loads(request.POST.get('passenger_fender_damage', False))
        driver_door_damage=json.loads(request.POST.get('driver_door_damage', False))
        passenger_door_damage=json.loads(request.POST.get('passenger_door_damage', False))
        driver_rear_door_damage=json.loads(request.POST.get('driver_rear_door_damage', False))
        passenger_rear_door_damage=json.loads(request.POST.get('passenger_rear_door_damage', False))
        driver_rocker_damage=json.loads(request.POST.get('driver_rocker_damage', False))
        passenger_rocker_damage=json.loads(request.POST.get('passenger_rocker_damage', False))
        driver_rear_wheel_arch_damage=json.loads(request.POST.get('driver_rear_wheel_arch_damage', False))
        passenger_rear_wheel_arch_damage=json.loads(request.POST.get('passenger_rear_wheel_arch_damage', False))
        driver_rear_quarter_damage=json.loads(request.POST.get('driver_rear_quarter_damage', False))
        passenger_rear_quarter_damage=json.loads(request.POST.get('passenger_rear_quarter_damage', False))
        trunk_damage=json.loads(request.POST.get('trunk_damage', False))
        rear_bumper_damage=json.loads(request.POST.get('rear_bumper_damage', False))
        driver_tail_light_damage=json.loads(request.POST.get('driver_tail_light_damage', False))
        passenger_tail_light_damage=json.loads(request.POST.get('passenger_tail_light_damage', False))
        driver_mirror_damage=json.loads(request.POST.get('driver_mirror_damage', False))
        passenger_mirror_damage=json.loads(request.POST.get('passenger_mirror_damage', False))
        windshield_damage=json.loads(request.POST.get('windshield_damage', False))
        driver_window_damage=json.loads(request.POST.get('driver_window_damage', False))
        passenger_window_damage=json.loads(request.POST.get('passenger_window_damage', False))
        driver_rear_window_damage=json.loads(request.POST.get('driver_rear_window_damage', False))
        passenger_rear_window_damage=json.loads(request.POST.get('passenger_rear_window_damage', False))
        back_glass_damage=json.loads(request.POST.get('back_glass_damage', False))
        truck_bed_damage=json.loads(request.POST.get('truck_bed_damage', False))


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
            sale_date=sale_date,
            creator=user,
            vehicle_starts=vehicle_starts,
            vehicle_drives=vehicle_drives,
            bumper_damage=bumper_damage,
            driver_headlight_damage=driver_headlight_damage,
            passenger_headlight_damage=passenger_headlight_damage,
            hood_damage=hood_damage,
            roof_damage=roof_damage,
            driver_fender_damage=driver_fender_damage,
            passenger_fender_damage=passenger_fender_damage,
            driver_door_damage=driver_door_damage,
            passenger_door_damage=passenger_door_damage,
            driver_rear_door_damage=driver_rear_door_damage,
            passenger_rear_door_damage=passenger_rear_door_damage,
            driver_rocker_damage=driver_rocker_damage,
            passenger_rocker_damage=passenger_rocker_damage,
            driver_rear_wheel_arch_damage=driver_rear_wheel_arch_damage,
            passenger_rear_wheel_arch_damage=passenger_rear_wheel_arch_damage,
            driver_rear_quarter_damage=driver_rear_quarter_damage,
            passenger_rear_quarter_damage=passenger_rear_quarter_damage,
            trunk_damage=trunk_damage,
            rear_bumper_damage=rear_bumper_damage,
            driver_tail_light_damage=driver_tail_light_damage,
            passenger_tail_light_damage=passenger_tail_light_damage,
            driver_mirror_damage=driver_mirror_damage,
            passenger_mirror_damage=passenger_mirror_damage,
            windshield_damage=windshield_damage,
            driver_window_damage=driver_window_damage,
            passenger_window_damage=passenger_window_damage,
            driver_rear_window_damage=driver_rear_window_damage,
            passenger_rear_window_damage=passenger_rear_window_damage,
            back_glass_damage=back_glass_damage,
            truck_bed_damage=truck_bed_damage
        )

        images = request.FILES.getlist('images')
        for i, image in enumerate(images):
            setattr(car, f"image_{i+1}", image)

        car.save()
        return JsonResponse({'success': True})
    else:
        return HttpResponseBadRequest('Invalid request method')
    
@requires_csrf_token
@api_view(['POST'])
def save_filter(request, user_id):
    data = json.loads(request.body)
    user = User.objects.get(pk=user_id)
    make = data['filters'].get('make')
    model = data['filters'].get('model')
    start_year = data['filters']['year'].get('start')
    end_year = data['filters']['year'].get('end')
    filter_name = data.get('name')

    filter, created = VehicleFilter.objects.get_or_create(user=user, make=make, model=model, start_year=start_year, end_year=end_year, filter_name=filter_name)
    if created:
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Filter already exists'})

def get_filters(request, user_id):
    user = User.objects.get(pk=user_id)
    filters = VehicleFilter.objects.filter(user=user)
    data = []
    for filter in filters:
        data.append({
            'id': filter.id,
            'make': filter.make,
            'model': filter.model,
            'start': filter.start_year,
            'end': filter.end_year,
            'name': filter.filter_name,
        })
    return JsonResponse({'filters': data})

@requires_csrf_token
@api_view(['POST'])
def declare_winner(request):
    data = json.loads(request.body)
    car = Car.objects.get(pk=data.get('carID'))
    bids = Bid.objects.filter(bid_vehicle=car)
    highest_bid = bids.order_by('-bid_amount').first()
    if highest_bid:
        user = User.objects.get(pk=highest_bid.bidder.id)

    if user:
        send_mail(
            'Congratulations from the SimpliCars Team!',
            f'Howdy {user.first_name},\n\nCongratulations on winning your {car.make} {car.model} with VIN {car.VIN}! Please contact us to arrange payment and pickup of the vehicle.\n\nBest regards,\nThe Auction Team',
            os.environ.get('GMAIL_EMAIL'),
            [user.email]
        )
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'User not found'})

def user_info(request, user_id):
    user = User.objects.get(pk=user_id)
    return JsonResponse({
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'is_staff': user.is_staff,
    })

@requires_csrf_token
@api_view(['POST'])
def update_user(request, user_id):
    data = json.loads(request.body)
    user = User.objects.get(pk=user_id)
    user.first_name = data.get('first_name')
    user.last_name = data.get('last_name')
    user.email = data.get('email')
    user.save()
    #return user data
    return JsonResponse({
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'is_staff': user.is_staff,
    })

def bid_history(request, user_id):
    user = User.objects.get(pk=user_id)
    bids = Bid.objects.filter(bidder=user)
    data = []
    for bid in bids:
        data.append({
            'id': bid.id,
            'bid_amount': bid.bid_amount,
            'bid_date': bid.bid_date.strftime('%d/%m/%Y'),
            'bid_vehicle': bid.bid_vehicle.VIN,
        })
    
    return JsonResponse({'bids': data})