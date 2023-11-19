# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import timedelta
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from django.utils import timezone


class BiddingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("bidding_group", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("bidding_group", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        if action == 'place_bid':
            updated_vehicle, bid = await self.update_vehicle_bid(data)
            await self.broadcast_updated_state(updated_vehicle, bid)

    async def broadcast_updated_state(self, car, bid):
        await self.channel_layer.group_send(
            "bidding_group",
            {
                "type": "update.message",
                "sale_date": car.sale_date.isoformat(),
                "bid_amount": bid.bid_amount,
            },
        )
    
    @database_sync_to_async
    def update_vehicle_bid(self, data):
        from .models import Bid
        from .models import Car
        # from .user import User
        from django.contrib.auth.models import User
        try:
            userID = data.get('user_id')
            vehicleVIN = data.get('vehicle_vin')
            bidAmount = data.get('bid_amount')
            car = Car.objects.get(VIN=vehicleVIN)
            user = User.objects.get(pk=userID)
            bid = Bid.objects.create(bid_amount=bidAmount, bidder=user, bid_vehicle=car)
            bid.save()
            time_remaining = car.sale_date - timezone.now()
            if time_remaining.total_seconds() < 30:
                car.sale_date = timezone.now() + timedelta(seconds=min(30, time_remaining.total_seconds() + 30))
            # else:
            #     car.sale_date = car.sale_date + timedelta(seconds=30)
            car.save()
            return car, bid
        except:
            print("Error updating vehicle bid")

    async def update_message(self, event):
        sale_date = event["sale_date"]
        bid_amount = event["bid_amount"]
        await self.send(text_data=json.dumps({
            'type': 'update',
            'sale_date': sale_date,
            'bid_amount': bid_amount,
        }))