
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from mechatronics.models import Equipo


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
def database_search(date_start, date_end, status):
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
