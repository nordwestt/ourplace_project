import base64
import math
import os
import pickle

import numpy

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'ourplace_project.settings')
import django
django.setup()
from ourplace.models import Canvas, UserProfile, CanvasAccess
from django.contrib.auth.models import User
from PIL import Image
import static.constants.colours as colours
def populate():
    #Start by creating lists of dictionaries of each entry required

    users = [
        {'username':'Christ', 'email':'jchrist@heaven.god', 'password':'imcross'},
        {'username':'Moses', 'email':'parting@water.god', 'password':"watern't"},
        {'username':'God', 'email':'god@god.god', 'password':'admin'},
        {'username':'John', 'email':'spreadingthe@word.god', 'password':'disciple12'},
        {'username':'Joe', 'email':'everyday@joe.com', 'password':'password'},
        {'username':'Matthew', 'email':'balding@hotmale.com', 'password':'alpecin'},
        {'username':'James', 'email':'jangus1@gmail.com', 'password':'twin'},
        {'username':'Angus', 'email':'jangusA@gmail.com', 'password':'twin'},
        {'username':'Thomas', 'email':'thomas@yahoo.com', 'password':'securepassword'},
    ]

    canvases = [ #if you want to add another image put it in the population images directory then add 'image':'image.png' to the canvas. Make sure the input image is the right size
        {'title':'The Long Table', 'size':50, 'owner':'Christ', 'colour_palette':1, 'visibility':'O','views':10},
        {'title':'The Loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooong Table', 'size':50, 'owner':'Moses', 'colour_palette':1, 'visibility':'O','views':5},
        {'title':'Earth', 'size':100, 'owner':'God', 'colour_palette':1, 'visibility':'O','views':20},
        {'title':'Heaven', 'size':200, 'owner':'God','colour_palette':0, 'visibility':'C','views':2},
        {'title':'The Beach', 'size':10, 'owner':'God','colour_palette':0, 'visibility':'O', 'image':'beach.png','views':100},
        {'title':'Our House', 'size':20, 'owner':'Matthew','colour_palette':0, 'visibility':'C', 'image':'our house.png','views':60},
    ]

    canvasaccess = [
        {'canvas':'Heaven', 'user':'Christ'},
        {'canvas':'Heaven', 'user':'Moses'},
        {'canvas':'Heaven', 'user':'John'},
        {'canvas':'Our House', 'user':'James'},
        {'canvas':'Our House', 'user':'Angus'},
        {'canvas':'Our House', 'user':'Thomas'},
    ]
    # adding our new items in to the databases
    # starting by deleting all the existing objets so we don't have any issues with unique fields
    for o in CanvasAccess.objects.all():
        o.delete()
    for o in Canvas.objects.all():
        o.delete()
    for o in UserProfile.objects.all():
        o.user.delete()
    #adding new users by creating new user objects, then using them to create new userprofile objects
    for i in users:
        newUser = User.objects.create_user(i['username'], i['email'], i['password'])
        newUserProfile = UserProfile(user =newUser)
        newUserProfile.save()

    #creating new blank canvases
    for canvas in canvases:
        u = User.objects.get_or_create(username=canvas['owner'])[0]
        c = Canvas.objects.get_or_create(title=canvas['title'], owner=u, size=canvas['size'], visibility=canvas['visibility'], views=canvas['views'])[0]
        c.colour_palette = canvas['colour_palette']
        c.save()
        if 'image' in canvas:
            imageToCanvas(c,canvas['image'])
            c.save()

    #setting up access rights by finding the correct canvas objects and the correct users then using them to create a new entry
    for i in canvasaccess:
        u = User.objects.get(username=i['user'])
        c = Canvas.objects.get(title=i['canvas'])
        ca = CanvasAccess(user=u,canvas=c)
        print(ca)
        ca.save()


    for c in Canvas.objects.all():
        print(str(c))
    for ca in CanvasAccess.objects.all():
        print(str(ca))
    for u in UserProfile.objects.all():
        print(str(u))

def imageToCanvas(canvas, imageLink):

    #filling out a blank canvas
    palette = [] # starting by making a palette
    indexfinder = {} #and a dictionary that maps the values in it to an index in colours.palette1
    for i in range(len(colours.palette1)):
        colour = colours.palette1[i][4:-1].split(", ") #grab the list of strings of ints
        colourtuple= (int(colour[0]), int(colour[1]), int(colour[2])) #put them in to a tuple of ints
        palette.append(colourtuple)# assign it to the list
        indexfinder[colourtuple] = i #and assign it to the dict with its index


    #now we have our palette we can open the image
    imageLocation = os.path.join("population_images", imageLink)
    im=Image.open(imageLocation)
    im=im.convert('RGB')
    width, height = im.size
    #need to set up the array to put the pixels in to
    nl = [[0 for i in range(width)] for i in range(height)]

    for x in range(width):
        for y in range(height):
            r,g,b=im.getpixel((x,y)) #get the rgb value at the current pixel
            nl[x][y] = indexfinder[findclosest(palette, (r,g,b))] #map it's closest equivalent in the palette to the equivalent position in the array


    bitmap_bytes = base64.b64encode(pickle.dumps(numpy.array(nl))) #convert it to a numpy array then a string version
    canvas.bitmap= bitmap_bytes#save it
    canvas.save()



def findclosest(palette, colourtofind):
    return min(palette, key=lambda x:distance(x,colourtofind))

def distance(c1, c2): #to calculate how close one colour is from the other
    (r1,g1,b1) = c1
    (r2,g2,b2) = c2
    return math.sqrt((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2)



#Startexecutionhere!
if __name__=='__main__':
    print('Starting Ourplace population script...')
    populate()
