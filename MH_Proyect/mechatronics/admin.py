# encoding:utf-8
# Agregamos modelos creados a nuestra django admin

from django.contrib import admin
from mechatronics.models import Equipo, Cliente, Empleado, Servicio, Pago


class ClienteAdmin(admin.ModelAdmin):
     # agrega los campos a visualizar como lista en el admin.
    list_display = ('nombre', 'apellido', 'telefono',
                    'direccion', 'email', 'registro')

    # crea una barra de filtrado del lado derecho de la lista.
    list_filter = ('registro',)

    # agregamos una barra de búsqueda.
    search_fields = ('nombre', 'apellido')

    # agregamos filtro basado en fechas.
    date_hierarchy = ('registro')

    # ordena los objetos del admin.
    ordering = ('registro',)

    # campos a visualizar al ingresar un cliente en el formulario.
    fields = (('nombre', 'apellido'), ('telefono', 'email'),
              ('direccion', 'rfc', 'razon_social'))


class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'telefono',
                    'email', 'estado', 'registro')
    list_filter = ('registro', 'estado')

    search_fields = ('nombre', 'apellido')
    date_hierarchy = ('registro')

    # campos a visualizar al ingresar un empleado al formulario.
    fields = (('nombre', 'apellido',), ('telefono', 'email'),
              ('direccion', 'estado'), ('salario_base', 'comision'))


class EquipoAdmin(admin.ModelAdmin):
    list_display = ('folio', 'cliente', 'tipo', 'ingreso',
                    'entrega', 'estatus', 'total', 'empleado')
    list_filter = ('ingreso', 'entrega')

    search_fields = ('entrega', 'folio')
    date_hierarchy = ('ingreso')

    ordering = ('entrega',)

    filter_horizontal = ('servicios',)

    raw_id_fields = ('cliente',)

    # fields=(('tipo','marca','modelo'), 'servicios', ('costo','pago'),
    #         ('cliente','empleado'), ('ingreso','entrega', 'registro') )

    fieldsets = (
        (
            None,
            {
                'fields': (('folio', 'cliente'), ('tipo', 'marca', 'modelo'),
                           ('servicios'), ('entrega', 'estatus', 'total'),
                           ('empleado', 'registro'))
            }
        ),
    )


class ServicioAdmin(admin.ModelAdmin):
    list_display = ('servicio', 'costo')
    list_filter = ('servicio',)


class PagoAdmin(admin.ModelAdmin):
    list_display = ('servicio', 'monto', 'fecha_de_pago',)
    list_filter = ('fecha_de_pago',)

    search_fields = ('fecha_de_pago',)
    date_hierarchy = ('fecha_de_pago')

admin.site.register(Equipo, EquipoAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Servicio, ServicioAdmin)
admin.site.register(Pago, PagoAdmin)
