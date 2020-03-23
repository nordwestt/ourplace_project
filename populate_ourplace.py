import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'ourplace_project.settings')
import django
django.setup() 
from ourplace.models import Canvas, UserProfile, CAnvasACcess
def populate():
    #Start by creating lists of dictionaries of each entry required

    users = [
        {'username':'Christ', 'email':'jchrist@heaven.god'}, 
        {'username':'Moses', 'email':'parting@water.god'},
        {'username':'God', 'email':'bigdog@god.god'},
        {'username':'John', 'email':'spreadingthe@word.god'}
    ]

    canvases = [
        {'title':'The Long Table', 'size':50, 'owner':'Christ', 'colour_palette':1,},
        {'title':'Earth', 'size':100, 'owner':'God', 'colour_pallete':2},
        {'title':'Heaven', 'size':200, 'owner':'God','colour_pallete':0}
    ]

    canvasaccess = [
        {'canvas':'The Long Table', 'user'='Christ'},
        {'canvas':'The Long Table', 'user'='John'},
        {'canvas':'The Long Table', 'user'='Moses'},
        {'canvas':'Earth', 'user'='God'},
        {'canvas':'Heaven', 'user'='God'},
        {'canvas':'Heaven', 'user'='Christ'},
        {'canvas':'Heaven', 'user'='Moses'},
        {'canvas':'Heaven', 'user'='John'},
    ]
    
    


# # First, we will create lists of dictionaries containing the pages
# # we want to add into each category.
# # Then we will create a dictionary of dictionaries for our categories. # This might seem a little bit confusing, but it allows us to iterate # through each data structure, and add the data to our models.
#     python_pages = [
# {'title': 'Official Python Tutorial',
# 'url':'http://docs.python.org/3/tutorial/'}, 
# {'title':'How to Think like a Computer Scientist',
# 'url':'http://www.greenteapress.com/thinkpython/'}, 
# {'title':'Learn Python in 10 Minutes',
# 'url':'http://www.korokithakis.net/tutorials/python/'} ]
#     django_pages = [
# {'title':'Official Django Tutorial', 
#  'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/'},
# {'title':'Django Rocks', 
#  'url':'http://www.djangorocks.com/'},
# {'title':'How to Tango with Django', 
#  'url':'http://www.tangowithdjango.com/'} ]
#     other_pages = [ {'title':'Bottle',
# 'url':'http://bottlepy.org/docs/dev/'},
#  {'title':'Flask',
# 'url':'http://flask.pocoo.org'} ]
#     cats = {'Python': {'pages': python_pages},
#             'Django': {'pages': django_pages},
#             'Other Frameworks': {'pages': other_pages} }
# # If you want to add more categories or pages, # add them to the dictionaries above.
# # The code below goes through the cats dictionary, then adds each category, # and then adds all the associated pages for that category.
#     for cat, cat_data in cats.items():
#         c = add_cat(cat)
#         for p in cat_data['pages']:
#             add_page(c, p['title'], p['url'])
# # Print out the categories we have added.
#     for c in Category.objects.all():
#         for p in Page.objects.filter(category=c):
#             print(f'- {c}: {p}')

#     for canvas in canvases:
#         c = add_canvas(canvas)

# def add_page(cat,title,url,views=0):
#     p = Page.objects.get_or_create(category=cat, title=title)[0] 
#     p.url=url
#     p.views=views
#     p.save()
#     return p
# def add_cat(name):
#     c = Category.objects.get_or_create(name=name)[0] 
#     c.save()
#     return c
# def add_canvas(name):
#     c = Canvas.objects.get_or_create(name=name)[0] 
#     c.save()
#     return c

#Startexecutionhere!
if __name__=='__main__':
    print('Starting Ourplace population script...') 
    populate()

