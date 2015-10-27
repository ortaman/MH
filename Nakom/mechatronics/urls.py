from django.conf.urls import patterns, url
from . import views


urlpatterns = [
    url(r'^administrativo/inicio$', views.index, name='index'),
]
