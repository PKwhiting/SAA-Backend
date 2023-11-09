import json
from simplicarbackend.car import Car
from simplicarbackend.car import AUCTION_CHOICES
from django.contrib.auth.models import User
# import django
# import os

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simplicarsaa.settings')
# django.setup()


# Load the JSON data from file
with open('copart.json') as f:
    car_data = json.load(f)

creator = User.objects.get(username='pattenwhiting')

for car in car_data:
    if car['vehicleCategory'] == 'Automobile' and car['saleDateTimeLeft']['isTimeLeft']:
        print(car)
        new_car = Car(
            auction=AUCTION_CHOICES[1][0],
            creator=creator,  # Replace with the creator of the car if applicable
            year=car['year'],
            make=car['make'],
            model=car['model'],
            VIN=car['vin'],
            title_code=car['title']['name'],
            color=car['color'],
            engine=car['engineSize'],
            engine_displacement=car['engineSize'],
            cylinders=car['cylinders'],
            transmission=car['transmission'],
            drive_type=car['drive'],
            vehicle_type=car['bodyStyle'],
            fuel_type=car['fuel'],
            keys=1,
            mileage=car['odometer'],
            starting_bid=0,
            current_bid=car['currentBid'],
            reserve_price=0,
            description=car['description'],
            # active=car['saleDateTimeLeft']['isTimeLeft'],
            # active=True,
            condition=f'{car["primaryDamage"]} {car["secondaryDamage"]}',
            vehicle_location=car['locationName'],
            sale_date=car['saleDate'],
            vehicle_auction_link = f'https://www.copart.com/lot/{car["id"]}',
            image_1_url = car['images'][0]['full'] if len(car['images']) > 0 else None,
            image_2_url = car['images'][1]['full'] if len(car['images']) > 1 else None,
            image_3_url = car['images'][2]['full'] if len(car['images']) > 2 else None,
            image_4_url = car['images'][3]['full'] if len(car['images']) > 3 else None,
            image_5_url = car['images'][4]['full'] if len(car['images']) > 4 else None,
            image_6_url = car['images'][5]['full'] if len(car['images']) > 5 else None,
            image_7_url = car['images'][6]['full'] if len(car['images']) > 6 else None,
            image_8_url = car['images'][7]['full'] if len(car['images']) > 7 else None,
            image_9_url = car['images'][8]['full'] if len(car['images']) > 8 else None,
            image_10_url = car['images'][9]['full'] if len(car['images']) > 9 else None,
            vehicle_starts=False,
            vehicle_drives=False
        )
        # Save the new Car object to the database
        new_car.save()