from django.conf.urls import url
from mechatronics import views


urlpatterns = [
    # url(r'^administrativo/$', views.login, name='login'),
    url(r'^administrative/index/$', views.index, name='index'),

    url(r'^administrative/equip/add/$', views.equip_add),
    url(r'^administrative/equip/search/$', views.equip_search),
    url(r'^administrative/equip/edit/(?P<id_equip>.*)/$', views.equip_edit),
    url(r'^administrative/equip/delete$', views.equip_delete),
]
