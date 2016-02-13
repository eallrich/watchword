from django.conf.urls import url

from ww.api import views

urlpatterns = [
    url(r'^ping/([0-9a-fA-F]+)', views.ping, name='ww-api-ping'),
    url(r'^status/([0-9a-fA-F]+)', views.status, name='ww-api-status'),
]
