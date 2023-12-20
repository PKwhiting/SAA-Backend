import json
from simplicarbackend.car import Car
from simplicarbackend.state import State
from simplicarbackend.car import AUCTION_CHOICES
from django.contrib.auth import get_user_model
User = get_user_model()
import django
import os
from django.conf import settings

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simplicarsaa.settings')
# django.setup()
def get_state(state_abbreviation):
    try:
        state = State.objects.get(state_abbr=state_abbreviation)
        return state
    except State.DoesNotExist:
        return None

# Load the JSON data from file
with open('copart.json') as f:
    car_data = json.load(f)

creator = User.objects.get(username='pattenwhiting')

for car in car_data:
    try:
        if car['vehicleCategory'] == 'Automobile' and car['saleDateTimeLeft']['isTimeLeft']:
            
            location = car.get('saleLocation', {})
            state_code = location.get('stateCode', '')
            state = get_state(state_code) if state_code else None
            buy_it_now_price=car.get('buyItNow', '')
            if int(buy_it_now_price) > 0:
                buy_it_now = True
            else:
                buy_it_now = False


            new_car = Car(
                auction=AUCTION_CHOICES[1][0],
                creator=creator,
                year=car.get('year', ''),
                make=car.get('make', ''),
                model=car.get('model', ''),
                VIN=car.get('vin', ''),
                title_classification="SALVAGE",
                title_note=car.get('title', {}).get('name', ''),
                color=car.get('color', ''),
                engine=car.get('engineSize', ''),
                engine_displacement=car.get('engineSize', ''),
                cylinders=car.get('cylinders', ''),
                transmission=car.get('transmission', ''),
                drive_type=car.get('drive', ''),
                vehicle_type=car.get('bodyStyle', ''),
                fuel_type=car.get('fuel', ''),
                buy_it_now_price=buy_it_now_price,
                buy_it_now = buy_it_now,
                keys=1,
                mileage=car.get('odometer', ''),
                odometer_brand='ACTUAL',
                starting_bid=0,
                current_bid=car.get('currentBid', ''),
                reserve_price=0,
                description=car.get('description', ''),
                condition=f'{car.get("primaryDamage", "")} {car.get("secondaryDamage", "")}',
                state=state,
                active=True,
                sale_date=car.get('saleDate', ''),
                vehicle_auction_link=f'https://www.copart.com/lot/{car["id"]}',
                image_1_url=car.get('images', [{}])[0].get('full', None),
                image_2_url=car.get('images', [{}])[1].get('full', None),
                image_3_url=car.get('images', [{}])[2].get('full', None),
                image_4_url=car.get('images', [{}])[3].get('full', None),
                image_5_url=car.get('images', [{}])[4].get('full', None),
                image_6_url=car.get('images', [{}])[5].get('full', None),
                image_7_url=car.get('images', [{}])[6].get('full', None),
                image_8_url=car.get('images', [{}])[7].get('full', None),
                image_9_url=car.get('images', [{}])[8].get('full', None),
                image_10_url=car.get('images', [{}])[9].get('full', None),
                vehicle_starts=False,
                vehicle_drives=False
            )
            new_car.save()
    except (TypeError, KeyError):
        print("ERROR")
        # print(TypeError, KeyError)