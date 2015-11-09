
from django.conf.urls import url

from mechatronics.views.login import index
from mechatronics.views.equip import equip_add, equip_search, equip_edit, equip_delete
from mechatronics.views import client

urlpatterns = [
    # url(r'^administrativo/$', views.login, name='login'),
    url(r'^administrative/index/$', index, name='index'),

    url(r'^administrative/equip/add/$', equip_add, name='add_equip'),
    url(r'^administrative/equip/search/$', equip_search, name='search_equip'),
    url(r'^administrative/equip/edit/(?P<id_equip>.*)/$', equip_edit, name='edit_equip'),
    url(r'^administrative/equip/delete$', equip_delete, name='delete_equip'),

    url(r'^administrative/client/add/$', client.add, name='add_client'),
    url(r'^administrative/client/search/$', client.search, name='search_client'),
    url(r'^administrative/client/edit/(?P<id_client>.*)/$', client.edit, name='edit_client'),
    url(r'^administrative/client/delete/$', client.delete, name='delete_client'),
]
