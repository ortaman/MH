# encoding:utf-8

from datetime import datetime, date

from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect

from mechatronics.models import Equipo
from mechatronics.forms import FormEquipo


def index(request):
    template_name = 'mechatronics/index.html'
    return render(request, template_name)


def equipment_add(request):
    error = str()
    if request.method == 'POST':

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
                    result = Equipo.objects.get(folio=folio)
                    form_equipment = FormEquipo(instance=result)

                except Equipo.DoesNotExist as exception:
                    error = "Folio: %s dosen't exist" % folio
                    form_equipment = FormEquipo()

            else:
                form_equipment = FormEquipo()

    # when load the web page use 'GET' method
    elif request.method == 'GET':
        form_equipment = FormEquipo()

    template_name = 'mechatronics/equipment_add.html'
    context = {'formEquip': form_equipment, 'error': error}
    return render(request, template_name, context)


def equipment_search(request):
    if request.method == 'GET':
        date_start = request.GET.get('textQuery1', '')
        date_end = request.GET.get('textQuery2', '')
        status = request.GET.get('textQuery3', '')

        # if the variable 'status' is empty '' the database ignore the
        # parameter (searching by date range).
        if date_start and date_end:
            date1 = datetime.strptime(date_start, '%d/%m/%Y')
            date1 = date1.strftime('%Y-%m-%d')

            date2 = datetime.strptime(date_end, '%d/%m/%Y')
            date2 = date2.strftime('%Y-%m-%d')

            result = Equipo.objects.filter(
                ingreso__range=(date1, date2),
                estatus__icontains=status)

        # searching by status
        elif status:
            result = Equipo.objects.filter(estatus__icontains=status)

        else:
            result = []

    template_name = 'mechatronics/equipment_search.html'
    ctx = {'result': result, 'date_start': date_start, 'date_end': date_end}
    return render(request, template_name, ctx)


def equipment_edit(request, id_equipment):
    # search by id and when load the web page to edit
    if request.method == 'GET':
        equipment = Equipo.objects.get(id=id_equipment)
        form_equipment = FormEquipo(instance=equipment)

        context = {'formEquip': form_equipment}
        template_name = 'mechatronics/equipment_add.html'

        return render(request, template_name, context)

    # save the changes in the equipment form
    elif request.method == 'POST':
        equipment = Equipo.objects.get(id=id_equipment)
        form_equipment = FormEquipo(request.POST, instance=equipment)

        if form_equipment.is_valid():
            form_equipment.save()
            url = '/administrative/equipment/search/'

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

    url = '/administrative/equipment/search/'
    return HttpResponseRedirect(url)
