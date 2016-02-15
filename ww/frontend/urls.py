from django.conf.urls import url

from ww.frontend import views

urlpatterns = [
    url(r'^$', views.index, name='ww-frontend-index'),
]
