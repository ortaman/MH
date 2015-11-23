# encoding:utf-8

from django.forms import ModelForm
from mechatronics.models import Equipo, Cliente, Empleado, Pago


''' class ModelForm permite crear un formulario a partir de un modelo'''


class FormEquipo(ModelForm):

    class Meta:
        model = Equipo
        fields = ['folio', 'tipo', 'marca', 'modelo',
                  'entrega', 'estatus', 'servicios',
                  'total', 'cliente', 'empleado', 'registro']


class FormCliente(ModelForm):

    class Meta:
        model = Cliente
        fields = '__all__'


class FormEmpleado(ModelForm):

    class Meta:
        model = Empleado
        fields = '__all__'


class FormPago(ModelForm):

    class Meta:
        model = Pago
        fields = '__all__'
