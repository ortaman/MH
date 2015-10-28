# encoding:utf-8

from django import forms
from django.forms import ModelForm
from mechatronics.models import Equipo


''' class ModelForm permite crear un formulario a partir de un modelo'''


class FormEquipo(ModelForm):

    class Meta:
        model = Equipo
        fields = ['folio', 'tipo', 'marca', 'modelo',
                  'entrega', 'estatus', 'servicios',
                  'total', 'cliente', 'empleado', 'registro']
