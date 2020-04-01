import json
import pickle
import base64
import numpy
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from ourplace.models import Canvas
import static.constants.colours as colours
from PIL import Image, ImageOps
from io import BytesIO
from django.core.files import File

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
            self.update_thumbnail(canvas, identical_copy)                    # calls the thumbnail generator
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

        im = Image.new("RGB", (canvas.size, canvas.size), 0) #creating a new image to start with
        pixels=im.load() #loading the pixels in to memory
        nestedlists=numpy.ndarray.tolist(bitmap_array) #converting the numpy array to a nested list
        for i in range(len(nestedlists)): #iterating through the array looking at each pixel individually
            for j in range(len(nestedlists)):
                if nestedlists[i][j] ==16: #a bodge fix for when the colour black is stored at 16 rather than 15 for some reason.
                    colourlist =colours.palette1[15][4:-1].split(", ") #finding the correct colour for this pizxel
                else:
                    colourlist =colours.palette1[nestedlists[i][j]][4:-1].split(", ") #finding the correct colour for this pizxel
                pixels[i,j]=(int(colourlist[0]), int(colourlist[1]), int(colourlist[2]))#writing that to the image 
        im = im.resize((255,255), resample=Image.NEAREST)
        blob=BytesIO()
        im.save(blob, 'PNG')
        canvas.thumbnail.save(canvas.slug+".png", File(blob), save=False)
    

    def make_thumbnail(self, canvas):
        bitmap_bytes = base64.b64decode(canvas.bitmap)
        bitmap_array = pickle.loads(bitmap_bytes)
        self.update_thumbnail(self, canvas, bitmap_array)
        canvas.save()