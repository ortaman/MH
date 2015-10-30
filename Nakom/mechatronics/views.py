# encoding:utf-8

from datetime import datetime, date

from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect

from mechatronics.models import Equipo
from mechatronics.forms import FormEquipo

from mechatronics.utilities import pagination


def index(request):
    template_name = 'mechatronics/index.html'
    return render(request, template_name)


def equipment_add(request):
    error = {}

    # when load the web page use 'GET' method
    if request.method == 'GET':
        form_equipment = FormEquipo()

    elif request.method == 'POST':

        # Add equipment
        if 'submitEquip' in request.POST:
            form_equipment = FormEquipo(request.POST)

            if form_equipment.is_valid():
                form_equipment.save()

                url = '/administrative/equipment/add/'
                return HttpResponseRedirect(url)

        # search equipment by folio
        elif 'submitFolio' in request.POST:
            folio = request.POST.get('folioQuery', '')

            if folio:
                try:
                    equipment = Equipo.objects.get(folio=folio)
                    form_equipment = FormEquipo(instance=equipment)

                except Equipo.DoesNotExist as exception:
                    error['search'] = "Folio: %s dosen't exist" % folio
                    form_equipment = FormEquipo()

            else:
                form_equipment = FormEquipo()

    template_name = 'mechatronics/equipment_add.html'
    context = {'formEquip': form_equipment, 'error': error}
    return render(request, template_name, context)


# search by date range and/or status and pagination
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


def equipment_search(request):
    if request.method == 'GET':
        q = {}
        per_page = 10
        page = request.GET.get('page')

        # equipment shearch
        if 'submitSearch' in request.GET and not page:
            q['date1'] = request.GET.get('queryDate1', '')
            q['date2'] = request.GET.get('queryDate2', '')
            q['status'] = request.GET.get('queryStatus', '')

        else:
            q['date1'] = request.GET.get('qdate1')
            q['date2'] = request.GET.get('qdate2')
            q['status'] = request.GET.get('qstatus')

        # searching by date range and/or status.
        equip_list = database_search(q['date1'], q['date2'], q['status'])
        equip_list = pagination(equip_list, page, per_page)

    template_name = 'mechatronics/equipment_search.html'
    ctx = {'equipList': equip_list, 'query': q}
    return render(request, template_name, ctx)


def equipment_edit(request, id_equipment):
    # search by id and when load the web page to edit
    if request.method == 'GET':
        equipment = Equipo.objects.get(id=id_equipment)
        form_equipment = FormEquipo(instance=equipment)

        p = request.GET.get('page', '')
        q = {}
        q['date1'] = request.GET.get('qdate1', '')
        q['date2'] = request.GET.get('qdate2', '')
        q['status'] = request.GET.get('qstatus', '')

        context = {'formEquip': form_equipment, 'query': q , 'page':p}
        template_name = 'mechatronics/equipment_add.html'

        return render(request, template_name, context)

    # save the changes in the equipment form
    elif request.method == 'POST':
        equipment = Equipo.objects.get(id=id_equipment)
        form_equipment = FormEquipo(request.POST, instance=equipment)

        if form_equipment.is_valid():
            form_equipment.save()

            p = request.POST.get('page', '')
            q1 = request.POST.get('queryDate1', '')
            q2 = request.POST.get('queryDate2', '')
            q3 = request.POST.get('queryStatus', '')
            print 'fsdfsdfsdfxzxcxc', p, q1, q2, q3

            url = '/administrative/equipment/search/'
            url += '?page=%s&qdate1=%s&qdate2=%s&qstatus=%s' % (p, q1, q2, q3)

        else:
            print 'Formulario no valido'
            url = '.'

    return HttpResponseRedirect(url)


def equipment_delete(request):
    if request.method == 'POST':
        delete = request.POST.getlist('delete')

        for id_equipo in delete:
            equipment = Equipo.objects.get(id=id_equipo)
            equipment.delete()

    p = request.POST.get('page', '')
    q1 = request.POST.get('queryDate1', '')
    q2 = request.POST.get('queryDate2', '')
    q3 = request.POST.get('queryStatus', '')

    url = '/administrative/equipment/search/'
    url += '?page=%s&qdate1=%s&qdate2=%s&qstatus=%s' % (p, q1, q2, q3)
    return HttpResponseRedirect(url)
