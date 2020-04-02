import base64
import json
import pickle

import numpy
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from ourplace.models import Canvas


class CanvasConsumer(WebsocketConsumer):

    def connect(self):
        self.place_name = self.scope['url_route']['kwargs']['place_name_slug']
        self.place_group_name = 'place_%s' % self.place_name

        # Join place group
        async_to_sync(self.channel_layer.group_add)(
            self.place_group_name,
            self.channel_name
        )

        self.accept()

    def receive(self, text_data):

        text_data_json = json.loads(text_data)
        x, y = text_data_json['x'], text_data_json['y']
        colour = text_data_json['colour']

        # Send message to place group
        async_to_sync(self.channel_layer.group_send)(
            self.place_group_name,
            {
                'type': 'canvas_update',
                'colour': colour,
                'x': x,
                'y': y
            }
        )


    def canvas_update(self, event):
        x, y = event['x'], event['y']
        colour = event['colour']

        try:
            canvas = Canvas.objects.get(slug=self.place_name)
            bitmap_bytes = base64.b64decode(canvas.bitmap)
            bitmap_array = pickle.loads(bitmap_bytes)
            identical_copy = numpy.copy(bitmap_array)
            # bitmap_array = pickle.loads(bitmap_bytes, mmap_mode="w+")
            identical_copy[x][y] = colour
            bitmap_bytes = base64.b64encode(pickle.dumps(identical_copy))
            setattr(canvas, "bitmap", bitmap_bytes)
            canvas.save()
            print("canvas updated!" + canvas.title)
        except Canvas.DoesNotExist:
            print("Canvas not found...")

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'colour': colour,
            'x': x,
            'y': y
        }))

    def disconnect(self, close_code):
        # Leave place group
        async_to_sync(self.channel_layer.group_discard)(
            self.place_group_name,
            self.channel_name
        )
