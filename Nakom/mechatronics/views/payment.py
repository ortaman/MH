# encoding:utf-8

from django.shortcuts import render
from django.http import HttpResponseRedirect

from mechatronics.models import Pago
from mechatronics.forms import FormPago
from mechatronics.utilities import pagination, payment_search


def add(request):
    if request.method == 'GET':
        form_payment = FormPago()

    elif request.method == 'POST':
        form_payment = FormPago(request.POST)

        if form_payment.is_valid():
            form_payment.save()
            form_payment = FormPago()
        else:
            print 'El pago no ha sido agregado: formulario inválido'

    template_name = 'mechatronics/payment_add.html'
    context = {'formPayment': form_payment}

    return render(request, template_name, context)


def search(request):
    # to search employee for the name or status or 'all' (show everyone).
    if request.method == 'GET':
        qdict = request.GET.dict()
        page = qdict.get('page')
        per_page = 10

        if 'submitSearch' in qdict or page:
            payment_list = payment_search(qdict)

        else:
            payment_list = []

        payment_list = pagination(payment_list, page, per_page)

    template_name = 'mechatronics/payment_search.html'
    context = {'paymentList': payment_list, 'q': qdict}

    return render(request, template_name, context)


def edit(request, id_payment):

    if request.method == 'GET':
        employee = Pago.objects.get(id=id_payment)
        form_payment = FormPago(instance=employee)

        qdict = request.GET.dict()
        template_name = 'mechatronics/payment_edit.html'
        context = {'formPayment': form_payment, 'q': qdict}

        return render(request, template_name, context)

    elif request.method == 'POST':
        payment = Pago.objects.get(id=id_payment)
        form_payment = FormPago(data=request.POST, instance=payment)

        if form_payment.is_valid():
            form_payment.save()

            qdict = request.POST.dict()
            values = (qdict['page'], qdict['date1'], qdict['date2'])

            url = '/administrative/payment/search/'
            url += '?page=%s&date1=%s&date2=%s' % values
        else:
            print 'El Pago no ha sido editado: fomulario no válido'

        return HttpResponseRedirect(url)


def delete(request):
    if request.POST == 'POST':
        ids_delete = request.POST.getlist('delete')

        for id_payment in ids_delete:
            payment = Pago.objects.get(id=id_payment)
            payment.delete()

    qdict = request.POST.dict()
    values = (qdict['page'], qdict['date1'], qdict['date2'])

    url = '/administrative/payment/search/'
    url += '?page=%s&date1=%s&date2=%s' % values

    return HttpResponseRedirect(url)
