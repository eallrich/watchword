from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^hq/', admin.site.urls),
    url(r'^',    include('ww.api.urls')),
    url(r'^',    include('ww.frontend.urls')),
]
