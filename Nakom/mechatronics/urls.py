from django.conf.urls import patterns, url
from mechatronics import views


urlpatterns = [
    #url(r'^administrativo/$', views.login, name='login'),
    url(r'^administrative/index/$', views.index, name='index'),

    url(r'^administrative/equipment/add/$', views.equipment_add),
    url(r'^administrative/equipment/search/$', views.equipment_search),
    url(r'^administrative/equipment/edit/(?P<id_equipment>.*)/$', views.equipment_edit),
    url(r'^administrative/equipment/delete$', views.equipment_delete),
]
