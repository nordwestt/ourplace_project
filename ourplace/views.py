from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required

import static.constants.colours as palettes

context_dict = {}

from ourplace.models import Canvas
from ourplace.forms import CanvasForm

def index(request):
    response = render(request, 'ourplace/index.html', context=context_dict)
    return response

def about(request):
    return render(request, 'ourplace/about.html', context=context_dict)

def faq(request):
    return render(request, 'ourplace/faq.html', context=context_dict)

@login_required
def account(request):
    return render(request, 'ourplace/account.html', context=context_dict)

def user(request):
    return render(request, 'ourplace/user.html', context=context_dict)

@login_required
def create_place(request):
    form = CanvasForm()
    context_dict['form'] = form

    # do we have a http post
    if request.method == 'POST':
        form = CanvasForm(request.POST)

        # is the form valid
        if form.is_valid():
            canvas = form.save(commit=False)
            canvas.owner = request.user
            canvas.save()
            return redirect(reverse('ourplace:index'))
        else:
            print(form.errors)
    return render(request, 'ourplace/create_place.html', context=context_dict)

def view_place(request, place_name_slug):
    context_dict = {}

    try:
        canvas = Canvas.objects.get(slug=place_name_slug)
        context_dict['canvas'] = canvas
    except Canvas.DoesNotExist:
        context_dict['canvas'] = None

    #increase total views for this place
    canvas.views=canvas.views+1

    palette = palettes.palette1
    context_dict['palette'] = palette



    return render(request, 'ourplace/view_place.html', context=context_dict)


def search(request):
    context_dict = {}

    if request.GET.get('q', False):
        search_string = request.GET['q']
        context_dict['has_searched'] = True
        context_dict['search_results'] = Canvas.objects.filter(title__contains=search_string)
        context_dict['num_results'] = len(context_dict['search_results'])
        context_dict['search_string'] = search_string

    try:
        if (request.user.is_authenticated):
            context_dict['users_places'] = Canvas.objects.filter(owner=request.user)
        context_dict['popular_places'] = Canvas.objects.order_by('views')[:8]
    except Canvas.DoesNotExist:
        context_dict['user_places'] = {}
    return render(request, 'ourplace/search.html', context=context_dict)

def download_bitmap(request, place_name_slug):
    response = {}
    try:
        canvas = Canvas.objects.get(slug=place_name_slug)
        bitmap_bytes = base64.b64decode(canvas.bitmap)
        bitmap_array = pickle.loads(bitmap_bytes)
        response['bitmap'] = bitmap_bytes
    except Canvas.DoesNotExist:
        raise Http404("Place not found..")

    return HttpResponse(json.dumps(response), content_type="application/json")
