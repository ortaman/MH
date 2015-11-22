# encoding:utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect

from mechatronics.models import Empleado
from mechatronics.forms import FormEmpleado
from mechatronics.utilities import pagination, employee_search


def add(request):
    if request.method == 'GET':
        form_employee = FormEmpleado()

    elif request.method == 'POST':
        form_employee = FormEmpleado(request.POST)

        if form_employee.is_valid():
            form_employee.save()
            form_employee = FormEmpleado()
        else:
            print 'El Empleado no ha sido agregado: formulario inválido'

    template_name = 'mechatronics/employee_add.html'
    context = {'formEmployee': form_employee}

    return render(request, template_name, context)


def search(request):
    # to search employee for the name or status or 'all' (show everyone).
    if request.method == 'GET':
        qdict = request.GET.dict()
        page = qdict.get('page')
        per_page = 10

        if 'submitSearch' in qdict or page:
            employee_list = employee_search(qdict)

        else:
            employee_list = []

        employee_list = pagination(employee_list, page, per_page)

    template_name = 'mechatronics/employee_search.html'
    context = {'employeeList': employee_list, 'query': qdict}

    return render(request, template_name, context)


def edit(request, id_employee):

    if request.method == 'GET':
        employee = Empleado.objects.get(id=id_employee)
        form_employee = FormEmpleado(instance=employee)

        qdict = request.GET.dict()
        template_name = 'mechatronics/employee_edit.html'
        context = {'formEmployee': form_employee, 'query': qdict}

        return render(request, template_name, context)

    elif request.method == 'POST':
        employee = Empleado.objects.get(id=id_employee)
        form_employee = FormEmpleado(data=request.POST, instance=employee)

        if form_employee.is_valid():
            form_employee.save()

            qdict = request.POST.dict()
            values = (qdict['page'], qdict['name'], qdict['status'])

            url = '/administrative/employee/search/'
            url += '?page=%s&name=%s&status=%s' % values
        else:
            print 'El Empleado no ha sido editado: fomulario no válido'

        return HttpResponseRedirect(url)


def delete(request):
    if request.POST == 'POST':
        ids_delete = request.POST.getlist('delete')

        for id_employee in ids_delete:
            employee = Empleado.objects.get(id=id_employee)
            employee.delete()

    qdict = request.POST.dict()
    values = (qdict['page'], qdict['name'], qdict['status'])

    url = '/administrative/employee/search/'
    url += '?page=%s&name=%s&status=%s' % values

    return HttpResponseRedirect(url)
