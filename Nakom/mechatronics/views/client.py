# encoding:utf-8
from datetime import date

from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseRedirect

from mechatronics.models import Cliente
from mechatronics.forms import FormCliente
from mechatronics.utilities import pagination


def add(request):
    if request.method == 'GET':
        form_client = FormCliente()

    elif request.method == 'POST':
        form_client = FormCliente(request.POST)

        if form_client.is_valid():
            form_client.save()
            form_client = FormCliente()
        else:
            print 'El cliente no ha sido agregado: formulario inválido'

    template_name = 'mechatronics/client_add.html'
    context = {'formClient': form_client}

    return render(request, template_name, context)


def search(request):
    # to search clients for the name or current month.
    if request.method == 'GET':
        qdict = request.GET.dict()
        per_page = 10

        if 'submitSearch' in qdict and not qdict.get('name'):
            name = qdict.get('name')
            query = Q(nombre__icontains=name) | Q(apellido__icontains=name)
            client_list = Cliente.objects.filter(query)
        else:
            month = date.today().month
            client_list = Cliente.objects.filter(registro__month=month)
            qdict['month'] = month

        client_list = pagination(client_list, qdict, per_page)

    template_name = 'mechatronics/client_search.html'
    context = {'clientList': client_list, 'query': qdict}

    return render(request, template_name, context)


def edit(request, id_client):

    if request.method == 'GET':
        client = Cliente.objects.get(id=id_client)
        form_client = FormCliente(instance=client)

        qdict = request.GET.dict()
        template_name = 'mechatronics/client_edit.html'
        context = {'formClient': form_client, 'query': qdict}

        return render(request, template_name, context)

    elif request.method == 'POST':
        client = Cliente.objects.get(id=id_client)
        form_client = FormCliente(data=request.POST, instance=client)

        if form_client.is_valid():
            form_client.save()

            qdict = request.POST.dict()
            values = (qdict['page'], qdict['name'], qdict['month'])

            url = '/administrative/client/search/'
            url += '?page=%s&name=%s&month=%s' % values
        else:
            print 'El cliente no ha sido editado: fomulario no válido'

        return HttpResponseRedirect(url)


def delete(request):
    if request.POST == 'POST':
        ids_delete = request.POST.getlist('delete')

        for id_client in ids_delete:
            client = Cliente.objects.get(id=id_client)
            client.delete()

    qdict = request.POST.dict()
    values = (qdict['page'], qdict['name'], qdict['month'])

    url = '/administrative/client/search/'
    url += '?page=%s&name=%s&month=%s' % values

    return HttpResponseRedirect(url)
