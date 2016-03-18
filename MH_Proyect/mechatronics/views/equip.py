# encoding:utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect

from mechatronics.models import Equipo
from mechatronics.forms import FormEquipo
from mechatronics.utilities import pagination, equip_search


def add(request):
    error = {}

    # when load the web page use 'GET' method
    if request.method == 'GET':
        form_equip = FormEquipo()

    elif request.method == 'POST':
        # search equip by folio
        if 'submitFolio' in request.POST:
            folio = request.POST.get('folioQuery')

            if folio:
                try:
                    equip = Equipo.objects.get(folio=folio)
                    form_equip = FormEquipo(instance=equip)
                except Equipo.DoesNotExist:
                    error['search'] = "Folio: %s dosen't exist" % folio
                    form_equip = FormEquipo()
            else:
                form_equip = FormEquipo()

        elif 'submitEquip' in request.POST:
            # Add equip (if 'formEquip' in request.POST:)
            form_equip = FormEquipo(request.POST)

            if form_equip.is_valid():
                form_equip.save()

                url = '/administrative/equip/add/'
                return HttpResponseRedirect(url)
            else:
                print 'EL formulario del equipo no es válido'

    template_name = 'mechatronics/equip_add.html'
    context = {'formEquip': form_equip, 'error': error}
    return render(request, template_name, context)


def search(request):
    # to search equipment for date range or status.
    if request.method == 'GET':
        page = request.GET.get('page')
        q = request.GET.dict()
        per_page = 10

        # equip shearch
        if 'submitSearch' in request.GET and not page:
            queryset = equip_search(q['date1'], q['date2'], q['status'])

        else:
            try:
                queryset = equip_search(q['date1'], q['date2'], q['status'])
            except KeyError:
                queryset = []

        queryset = pagination(queryset, page, per_page)

    template_name = 'mechatronics/equip_search.html'
    ctx = {'equipList': queryset, 'query': q}

    return render(request, template_name, ctx)


def edit(request, id_equip):
    # search by id and when load the web page to edit
    if request.method == 'GET':
        equip = Equipo.objects.get(id=id_equip)
        form_equip = FormEquipo(instance=equip)

        template_name = 'mechatronics/equip_edit.html'
        query_dict = request.GET.dict()
        context = {'formEquip': form_equip, 'query': query_dict}

        return render(request, template_name, context)

    # save the changes in the equip form
    elif request.method == 'POST':
        equip = Equipo.objects.get(id=id_equip)
        form_equip = FormEquipo(request.POST, instance=equip)

        if form_equip.is_valid():
            form_equip.save()

            qdict = request.POST.dict()
            values = (qdict['page'], qdict['date1'], qdict['date2'], qdict['status'])

            url = '/administrative/equip/search/'
            url += '?page=%s&date1=%s&date2=%s&status=%s' % values
        else:
            print 'El formulario del cliente no ha sido válido'
            url = '.'

    return HttpResponseRedirect(url)


def delete(request):
    if request.method == 'POST':
        delete = request.POST.getlist('delete')

        for id_equipo in delete:
            equip = Equipo.objects.get(id=id_equipo)
            equip.delete()

    qdict = request.POST.dict()
    values = (qdict['page'], qdict['date1'], qdict['date2'], qdict['status'])

    url = '/administrative/equip/search/'
    url += '?page=%s&date1=%s&date2=%s&status=%s' % values

    return HttpResponseRedirect(url)
