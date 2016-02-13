from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^hq/', include(admin.site.urls)),
    url(r'^',       include('ww.api.urls')),
]
