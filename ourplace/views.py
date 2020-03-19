from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

context_dict = {'signed_in': True}

from ourplace.models import Canvas
from ourplace.forms import CanvasForm

def index(request):
    response = render(request, 'ourplace/index.html', context=context_dict)
    return response

def about(request):
    return render(request, 'ourplace/about.html', context=context_dict)

def faq(request):
    return render(request, 'ourplace/faq.html', context=context_dict)

def login(request):
    return render(request, 'ourplace/login.html', context=context_dict)

def account(request):
    return render(request, 'ourplace/account.html', context=context_dict)

def user(request):
    return render(request, 'ourplace/user.html', context=context_dict)

def create_place(request):
    form = CanvasForm()
    context_dict['form'] = form

    # do we have a http post
    if request.method == 'POST':
        form = CanvasForm(request.POST)

        # is the form valid
        if form.is_valid():
            form.save(commit=True)  #
            return redirect('/ourplace/')
        else:
            print(form.errors)
    return render(request, 'ourplace/create_place.html', context=context_dict)

def view_place(request):
    return render(request, 'ourplace/view_place.html', context=context_dict)


def show_canvas(request, canvas_name_slug): 
    # Create a context dictionary which we can pass 
    # # to the template rendering engine. 
    context_dict = {}

    try:
        # Can we find a category name slug with the given name? 
        # # If we can't, the .get() method raises a DoesNotExist exception. 
        # # The .get() method returns one model instance or raises an exception. 
        canvas = Canvas.objects.get(slug=canvas_name_slug)
        
        context_dict['canvas'] = canvas 
    except Canvas.DoesNotExist: 
        # We get here if we didn't find the specified category. 
        # Don't do anything 
        # the template will display the "no category" message for us. 
        context_dict['canvas'] = None 

    colours = [["rgb(255, 255, 255)","rgb(255, 255, 0)", "rgb(255, 102, 0)", "rgb(221, 0, 0)"], ["rgb(255, 0, 153)",
    "rgb(51, 0, 153)","rgb(0, 0, 204)","rgb(0, 153, 255)"], ["rgb(0, 170, 0)", "rgb(0, 102, 0)","rgb(102, 51, 0)",
    "rgb(153, 102, 51)"],["rgb(187, 187, 187)","rgb(136, 136, 136)","rgb(68, 68, 68)","rgb(0, 0, 0)"]]

    context_dict['colours'] = colours

    # Go render the response and return it to the client. 
    return render(request, 'ourplace/canvas.html', context=context_dict)
def search(request):
    return render(request, 'ourplace/search.html', context=context_dict)
