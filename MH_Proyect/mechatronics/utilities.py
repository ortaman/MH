
from datetime import datetime, date

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from mechatronics.models import Equipo, Cliente, Empleado, Pago


def pagination(objects_list, page, objects_per_page=10):
    paginator = Paginator(objects_list, objects_per_page)

    try:
        objects_list = paginator.page(page)

    except PageNotAnInteger:
        objects_list = paginator.page(1)

    except EmptyPage:
        objects_list = paginator.page(paginator.num_pages)

    return objects_list


# search by date range and/or
def equip_search(date_start, date_end, status):
    # search by date range
    if date_start and date_end:
        date1 = datetime.strptime(date_start, '%d/%m/%Y').strftime('%Y-%m-%d')
        date2 = datetime.strptime(date_end, '%d/%m/%Y').strftime('%Y-%m-%d')

        equip_list = Equipo.objects.filter(ingreso__range=(date1, date2),
                                           estatus__icontains=status)

    # searching by status
    elif status:
        equip_list = Equipo.objects.filter(estatus__icontains=status)

    # date and status are empty
    else:
        equip_list = []

    return equip_list


def client_search(qdict):
    name = qdict.get('name')

    if name:
        query = Q(nombre__icontains=name) | Q(apellido__icontains=name)
        client_list = Cliente.objects.filter(query)
    else:
        month = date.today().month
        client_list = Cliente.objects.filter(registro__month=month)
        qdict['month'] = month

    return client_list


def employee_search(qdict):
    name = qdict.get('name')
    status = qdict.get('status')

    if name == 'all':
        employee_list = Empleado.objects.all()

    elif name and not status:
        query = Q(nombre__icontains=name) | Q(apellido__icontains=name)
        employee_list = Empleado.objects.filter(query)

    elif not name and status:
        employee_list = Empleado.objects.filter(estado=status)

    else:
        query = Q(nombre__icontains=name) | Q(apellido__icontains=name)
        query = query & Q(estado=status)
        employee_list = Empleado.objects.filter(query)

    return employee_list


def payment_search(qdict):
    date1 = qdict.get('date1')
    date2 = qdict.get('date2')

    # search by date range
    if date1 and date2:
        date1 = datetime.strptime(date1, '%d/%m/%Y').strftime('%Y-%m-%d')
        date2 = datetime.strptime(date2, '%d/%m/%Y').strftime('%Y-%m-%d')

        payment_list = Pago.objects.filter(fecha_de_pago__range=(date1, date2))

    else:
        payment_list = []

    return payment_list
