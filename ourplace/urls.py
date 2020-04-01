
from django.urls import path
from ourplace import views
from django.contrib.sitemaps.views import sitemap
from .sitemap import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

app_name = 'ourplace'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('account/', views.account, name='account'),
    path('user/<str:username>/', views.user, name='user'),
    path('place/', views.create_place, name='create_place'),
    path('place/edit/<str:place_name_slug>/', views.edit_place, name='edit_place'),
    path('place/access/<str:place_name_slug>/', views.access_place, name='edit_place_access'),
    path('place/<str:place_name_slug>/', views.view_place, name='view_place'),
    path('search/', views.search, name='search'),
    path('bitmap/<str:place_name_slug>/', views.download_bitmap, name='download_bitmap'),
    path('sitemap.xml', sitemap, {'sitemaps':sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
