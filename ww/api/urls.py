from django.conf.urls import url

from ww.api import views

urlpatterns = [
    url(r'^ping/([0-9a-fA-F]{10})/?$', views.ping, name='ww-api-ping'),
    url(r'^status/([0-9a-fA-F]{10})/?$', views.status, name='ww-api-status'),
    url(r'^api/watches/$', views.watches_list, name='ww-api-watches-list'),
]
