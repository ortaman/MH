from django.conf.urls import patterns, url
from . import views


urlpatterns = [
    url(r'^administrativo/$', views.index, name='index'),
]
