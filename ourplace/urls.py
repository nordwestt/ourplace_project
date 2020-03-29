
from django.urls import path
from ourplace import views

app_name = 'ourplace'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    ##path('canvas/<str:canvas_name_slug>/', views.show_canvas, name='show_canvas'),
    path('faq/', views.faq, name='faq'),
    path('account/', views.account, name='account'),
    path('user/{username}/', views.user, name='user'),
    path('place/', views.create_place, name='create_place'),
    path('place/<str:place_name_slug>/', views.view_place, name='view_place'),
    path('search/', views.search, name='search'),
    path('bitmap/<str:place_name_slug>/', views.download_bitmap, name='download_bitmap')
]
