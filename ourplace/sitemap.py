from django.contrib import sitemaps
from django.urls import reverse
from . import urls

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return urls.urlpatterns

    def location(self, item):
        return "/" + str(item.pattern)
