import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class CanvasConsumer(WebsocketConsumer):
    #groups = ["broadcast"]

    def connect(self):
        self.accept()


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        x, y = text_data_json['x'], text_data_json['y']
        colour = text_data_json['colour']

        print("x, y: "+str(x)+', '+str(y))
        print("colour: "+colour)
#        self.send(text_data=json.dumps({
 #           'message': message
  #      }))

    def disconnect(self, close_code):
        # Called when the socket closes
        pass