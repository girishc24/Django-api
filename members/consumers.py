from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Device
from django.http import HttpResponse
import json

class ChatConsumer(AsyncWebsocketConsumer):


    async def connect(self):
        
        device_id = self.scope['url_route']['kwargs']['device_id']
        channel_id = self.channel_name    

        await self.accept()

        json_data = await self.create_device(channel_id, device_id)
        if json_data is not None:
            await self.send(text_data=json_data)
                   
        

    

    @database_sync_to_async
    def create_device(self, channel_id, device_id):
        device = Device.objects.create(channel_name=channel_id, device_id=device_id)
        device_data = {
        'channel_name': device.channel_name,
        'device_id': device.device_id
        }
        json_data = json.dumps(device_data)
        #print(json_data)
        return json_data
        
        
    async def disconnect(self, close_code):
        
        pass

   
    async def receive(self, text_data):
        await self.send(text_data="Hello world!")

    
