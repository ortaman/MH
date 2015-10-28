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
    template_name = 'mechatronics/equipment_add.html'

    if request.method == 'POST':
        form_equipment = FormEquipo(request.POST)

        if form_equipment.is_valid():
            form_equipment.save()

            url = '/administrative/equipment/add'
            return HttpResponseRedirect(url)

    else:
        form_equipment = FormEquipo()
        print 'GGGGEEEEEETTTT'

    template_name = 'mechatronics/equipment_add.html'
    context = {'formE': form_equipment}
    return render(request, template_name, context)


def equipment_search(request):

    if request.method == 'GET':
        date_start = request.GET.get('textQuery1', '')
        date_end = request.GET.get('textQuery2', '')
        status = request.GET.get('textQuery3', '')

        # if the variable 'status' is empty '' the database ignore the
        # parameter.
        if date_start and date_end:
            date1 = datetime.strptime(date_start, '%d/%m/%Y')
            date1 = date1.strftime('%Y-%m-%d')

            date2 = datetime.strptime(date_end, '%d/%m/%Y')
            date2 = date2.strftime('%Y-%m-%d')

            result = Equipo.objects.filter(
                ingreso__range=(date1, date2),
                estatus__icontains=status)

        elif not date_start and not date_end and status:
            result = Equipo.objects.filter(estatus__icontains=status)

        else:
            result = []

    template_name = 'mechatronics/equipment_search.html'
    ctx = {'result': result, 'date_start': date_start, 'date_end': date_end}
    return render(request, template_name, ctx)
