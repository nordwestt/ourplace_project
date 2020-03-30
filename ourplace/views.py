from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

import static.constants.colours as palettes

from django.contrib.auth.models import User
from ourplace.models import Canvas, UserProfile
from ourplace.forms import CanvasForm

def index(request):
    response = render(request, 'ourplace/index.html')
    return response

def about(request):
    return render(request, 'ourplace/about.html', context=context_dict)

def faq(request):
    return render(request, 'ourplace/faq.html')

@login_required
def account(request):
    return render(request, 'ourplace/account.html')

def user(request, username):
    context_dict = {}

    try:
        target_user = User.objects.get(username=username)
        context_dict['target_users_places'] = Canvas.objects.filter(owner=target_user).order_by('-views')
        context_dict['num_target_users_places'] = len(context_dict['target_users_places'])
        context_dict['target_user_total_views'] = context_dict['target_users_places'].aggregate(Sum('views'))['views__sum']
        context_dict['target_user'] = target_user
        # context_dict['target_user_profile'] = UserProfile.objects.get(user=target_user)
    except User.DoesNotExist:
        context_dict['target_user'] = None

    return render(request, 'ourplace/user.html', context=context_dict)

@login_required
def create_place(request):
    form = CanvasForm()
    context_dict = {}

    # do we have a http post
    if request.method == 'POST':
        form = CanvasForm(request.POST)

        # is the form valid
        if form.is_valid():
            canvas = form.save(commit=False)
            canvas.owner = request.user
            canvas.save()
            return redirect(reverse('ourplace:view_place', args=[canvas.slug]))
        # else:
        #     print(form.errors)

    # This is needed to allow the form to automagically display in two columns
    if len(list(form)) % 2 == 1:
        list(form).append(None)

    context_dict['form'] = zip(*[iter(form)]*2)

    return render(request, 'ourplace/create_place.html', context=context_dict)

def view_place(request, place_name_slug):
    context_dict = {}

    try:
        canvas = Canvas.objects.get(slug=place_name_slug)
        context_dict['canvas'] = canvas
        Canvas.objects.filter(slug=place_name_slug).update(views=canvas.views+1)
    except Canvas.DoesNotExist:
        context_dict['canvas'] = None

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
            context_dict['num_user_places'] = len(context_dict['users_places'])

        context_dict['popular_places'] = Canvas.objects.order_by('-views')[:8]
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
