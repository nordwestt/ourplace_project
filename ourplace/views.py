from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

import static.constants.colours as palettes

context_dict = {'signed_in': True}

from ourplace.models import Canvas


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
    return render(request, 'ourplace/create_place.html', context=context_dict)

def view_place(request, place_name_slug):
    context_dict = {}

    try:
        canvas = Canvas.objects.get(slug=place_name_slug)
        context_dict['canvas'] = canvas
    except Canvas.DoesNotExist: 
        context_dict['canvas'] = None 

    palette = palettes.palette1 
    
    context_dict['palette'] = palette


    return render(request, 'ourplace/view_place.html', context=context_dict)


def search(request):
    return render(request, 'ourplace/search.html', context=context_dict)
