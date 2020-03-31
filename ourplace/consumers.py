import json
import pickle
import base64
import numpy
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from ourplace.models import Canvas
import static.constants.colours as colours
from PIL import Image

class CanvasConsumer(WebsocketConsumer):
    #groups = ["broadcast"]

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
                'y':y
            }
        )

        print("x, y: "+str(x)+', '+str(y))
        print("colour: "+str(colour))


    def canvas_update(self, event):
        x, y = event['x'], event['y']
        colour = event['colour']

        try:
            canvas = Canvas.objects.get(slug=self.place_name)
            bitmap_bytes = base64.b64decode(canvas.bitmap)
            bitmap_array = pickle.loads(bitmap_bytes)
            identical_copy = numpy.copy(bitmap_array)
            #bitmap_array = pickle.loads(bitmap_bytes, mmap_mode="w+")
            identical_copy[x][y] = colour
            # self.update_thumbnail(canvas, identical_copy)                    # this would call the thumbnail generator, if it worked
            bitmap_bytes = base64.b64encode(pickle.dumps(identical_copy))
            setattr(canvas, "bitmap", bitmap_bytes)
            canvas.save()
            print("canvas updated!"+canvas.title)
        except Canvas.DoesNotExist: 
            print("Canvas not found...")

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'colour': colour,
            'x' : x,
            'y': y
        }))


    def disconnect(self, close_code):
        # Leave place group
        async_to_sync(self.channel_layer.group_discard)(
            self.place_group_name,
            self.channel_name
        )

    def update_bitmap(self, x, y, colour_val):

        try:
            canvas = Canvas.objects.get(slug=place_name_slug)
            bitmap_bytes = base64.b64decode(canvas.bitmap)
            bitmap_array = pickle.loads(bitmap_bytes)

            bitmap_array[x][y] = colour;
            np_bytes = pickle.dumps(bitmap_array)
            canvas.bitmap = base64.b64encode(np_bytes)
            bitmap_bytes = base64.b64decode(canvas.bitmap)
            bitmap_array = pickle.loads(bitmap_bytes)
            response['bitmap']   = bitmap_bytes
        except Canvas.DoesNotExist:
            raise Http404("Place not found..")

        return HttpResponse(json.dumps(response), content_type="application/json")
    
    def update_thumbnail(self, canvas, bitmap_array):
        print(canvas)
        newarray = numpy.copy(numpy.transpose(bitmap_array)) #creating a copy of the bitmap array to work on 
        print(newarray)
        nestedlists=numpy.ndarray.tolist(newarray) #converting it to a nested list
        for i in range(len(nestedlists)):
            for j in range(len(nestedlists)):
                print(nestedlists[i][j])
                nestedlists[i][j] = (colours.palette1[nestedlists[i][j]][4:-1]).split(", ") #swappig each colour int with its rgb value 
        print(nestedlists)
        newarray=numpy.array(nestedlists) #converting back to numpy
        print(newarray)
        img = Image.fromarray(newarray, 'RGB') #converting to image
        img.save('thumbnail.png')
        img.show()
