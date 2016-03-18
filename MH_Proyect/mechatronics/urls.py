
from django.conf.urls import url

from mechatronics.views.login import index
from mechatronics.views import equip, client, employee, payment

urlpatterns = [
    # url(r'^administrativo/$', views.login, name='login'),
    url(r'^administrative/index/$', index, name='index'),

    url(r'^administrative/equip/add/$', equip.add, name='equip-add'),
    url(r'^administrative/equip/search/$', equip.search, name='equip-search'),
    url(r'^administrative/equip/edit/(?P<id_equip>.*)/$', equip.edit, name='equip-edit'),
    url(r'^administrative/equip/delete/$', equip.delete, name='equip-delete'),

    url(r'^administrative/client/add/$', client.add, name='client-add'),
    url(r'^administrative/client/search/$', client.search, name='client-search'),
    url(r'^administrative/client/edit/(?P<id_client>.*)/$', client.edit, name='client-search'),
    url(r'^administrative/client/delete/$', client.delete, name='client-delete'),

    url(r'^administrative/employee/add/$', employee.add, name='employee-add'),
    url(r'^administrative/employee/search/$', employee.search, name='employee-search'),
    url(r'^administrative/employee/edit/(?P<id_employee>.*)/$', employee.edit, name='employee-edit'),
    url(r'^administrative/employee/delete/$', employee.delete, name='employee-delete'),

    url(r'^administrative/payment/add/$', payment.add, name='payment-add'),
    url(r'^administrative/payment/search/$', payment.search, name='payment-search'),
    url(r'^administrative/payment/edit/(?P<id_payment>.*)/$', payment.edit, name='payment-edit'),
    url(r'^administrative/payment/delete/$', payment.delete, name='payment-delete'),
]

