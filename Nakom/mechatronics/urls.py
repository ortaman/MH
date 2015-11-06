from django.conf.urls import url
from mechatronics import views


urlpatterns = [
    # url(r'^administrativo/$', views.login, name='login'),
    url(r'^administrative/index/$', views.index, name='index'),

    url(r'^administrative/equip/add/$', views.equip_add, name='add_equip'),
    url(r'^administrative/equip/search/$', views.equip_search, name='search_equip'),
    url(r'^administrative/equip/edit/(?P<id_equip>.*)/$', views.equip_edit, name='edit_equip'),
    url(r'^administrative/equip/delete$', views.equip_delete, name='delete_equip'),
]
