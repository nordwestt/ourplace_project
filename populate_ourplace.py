import os 
import numpy
import pickle
import base64
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'ourplace_project.settings')
import django
django.setup() 
from ourplace.models import Canvas, UserProfile, CanvasAccess
from django.contrib.auth.models import User
def populate():
    #Start by creating lists of dictionaries of each entry required

    users = [
        {'username':'Christ', 'email':'jchrist@heaven.god', 'password':'imcross'}, 
        {'username':'Moses', 'email':'parting@water.god', 'password':"watern't"},
        {'username':'God', 'email':'god@god.god', 'password':'admin'},
        {'username':'John', 'email':'spreadingthe@word.god', 'password':'disciple12'}
    ]

    canvases = [
        {'title':'The Long Table', 'size':50, 'owner':'Christ', 'colour_palette':1,},
        {'title':'Earth', 'size':100, 'owner':'God', 'colour_palette':2},
        {'title':'Heaven', 'size':200, 'owner':'God','colour_palette':0}
    ]

    canvasaccess = [
        {'canvas':'The Long Table', 'user':'Christ'},
        {'canvas':'The Long Table', 'user':'John'},
        {'canvas':'The Long Table', 'user':'Moses'},
        {'canvas':'Earth', 'user':'God'},
        {'canvas':'Heaven', 'user':'God'},
        {'canvas':'Heaven', 'user':'Christ'},
        {'canvas':'Heaven', 'user':'Moses'},
        {'canvas':'Heaven', 'user':'John'},
    ]
    # adding our new items in to the databases
    # starting by deleting all the existing objets so we don't have any issues with unique fields
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
        c = Canvas.objects.get_or_create(title=canvas['title'], owner=u, size=canvas['size'])[0]
        c.colour_palette = canvas['colour_palette']
        c.save()

    #setting up access rights by finding the correct canvas objects and the correct users then using them to create a new entry
    for i in canvasaccess:
        u = User.objects.get(username=i['user'])
        up = UserProfile.objects.get(user=u)
        c = Canvas.objects.get(title=i['canvas'])
        ca = CanvasAccess(user=up,canvas=c)
        ca.save()




    for c in Canvas.objects.all():
        print(str(c))
    for ca in CanvasAcess.objects.all():
        print(str(ca))
    for u in UserProfile.objects.all():
        print(str(u))

#Startexecutionhere!
if __name__=='__main__':
    print('Starting Ourplace population script...') 
    populate()

