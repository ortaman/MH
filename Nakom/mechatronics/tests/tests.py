# encoding:utf-8

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.utils import setup_test_environment

from mechatronics.models import Equipo

# needed to see response contex
setup_test_environment()


class IndexViewTests(TestCase):
    '''
    when the index page is accessed
    '''

    def setUp(self):
        self.url_index = '/administrative/index/'

    def test_status_code(self):
        self.response = self.client.get(self.url_index)
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        self.response = self.client.get(self.url_index)
        template_name = 'mechatronics/index.html'
        self.assertTemplateUsed(self.response, template_name)


# ******************   Test to add equipment view   ********************
class EquipAddViewTestGET(TestCase):
    '''
    When we have access in the page the first time,
    a formEquip empty.
    '''
    fixtures = ['initial_data.json']

    def setUp(self):
        self.template_name = 'mechatronics/equip_add.html'
        self.url_add = reverse('mechatronics:add_equip')
        self.response = self.client.get(self.url_add)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_form_equip_dict(self):
        self.assertTrue('formEquip' in self.response.context)
        self.assertFalse(self.response.context['formEquip'].is_bound)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, self.template_name)

    def test_error_dict(self):
        self.assertTrue('error' in self.response.context)
        self.assertEqual(self.response.context['error'], {})


class EquipAddViewTestPostSubmitSuccessful(TestCase):
    '''
    When we have added a equipment successfully.
    '''
    fixtures = ['initial_data.json']

    def setUp(self):
        self.template_name = 'mechatronics/equip_add.html'

        self.url_add = reverse('mechatronics:add_equip')
        self.equip = {
            "folio": "22", "registro": '1', "estatus": "almacenado",
            "tipo": "Televisi\u00f3n", "empleado": '2', "marca": "Sony",
            "servicios": [3, 4], "entrega": "2015-10-30", "modelo": "SmartTV",
            "total": 455.0, "cliente": '2', 'submitEquip': 'Buscar'}

    def test_status_code(self):
        response = self.client.post(self.url_add, self.equip, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_form_equip_dict(self):
        response = self.client.post(self.url_add, self.equip, follow=True)
        form_equip = response.context['formEquip']
        self.assertEqual(form_equip['folio'].value(), None)
        self.assertEqual(form_equip.instance.folio, '')

    def test_error_dict(self):
        response = self.client.post(self.url_add, self.equip, follow=True)
        self.assertTrue('error' in response.context)
        self.assertEqual(response.context['error'], {})

    def test_data_base(self):
        self.assertEqual(Equipo.objects.count(), 11)
        self.client.post(self.url_add, self.equip, follow=True)
        self.assertEqual(Equipo.objects.count(), 12)

    def test_http_response_redirect(self):
        response = self.client.post(self.url_add, self.equip, follow=False)
        self.assertEqual(response.status_code, 302)


class EquipAddViewTestPostSubmitUnsuccessfull(TestCase):
    '''
    When we have added a equipment unsucesully.
    '''
    fixtures = ['initial_data.json']

    def setUp(self):
        self.template_name = 'mechatronics/equip_add.html'

        self.url_add = reverse('mechatronics:add_equip')
        self.equip = {
            "folio": "22", "registro": '1', "estatus": "almacenado",
            "tipo": "Televisi\u00f3n", "empleado": '2', "marca": "Sony",
            "servicios": [3, 4], "entrega": "2015-10-30", "modelo": "SmartTV",
            "total": 455.0, "cliente": '2', 'submitEquip': 'Buscar'}

    def test_add_equip_with_folio_that_already_exit(self):
        response = self.client.post(self.url_add, self.equip, follow=True)
        response = self.client.post(self.url_add, self.equip, follow=True)
        error = 'Ya existe un/a Equipo con este/a Folio.'
        self.assertFormError(response, 'formEquip', 'folio', error)

    def test_add_equip_without_fields_data(self):
        data = {'submitEquip': 'Buscar'}
        response = self.client.post(self.url_add, data, follow=True)

        error = 'Este campo es obligatorio.'
        for key in self.equip:
            if not key == 'submitEquip':
                self.assertFormError(response, 'formEquip', key, error)

    def test_add_equip_with_date_field_format_invalid(self):
        self.equip['entrega'] = '11/11/111'
        response = self.client.post(self.url_add, self.equip, follow=True)
        error = u'Introduzca una fecha válida.'
        self.assertFormError(response, 'formEquip', 'entrega', error)


class EquipAddViewTestPostSearchFounded(TestCase):
    '''
    When searching a equip by folio and is foundeded.
    '''
    fixtures = ['initial_data.json']

    def setUp(self):
        self.template_name = 'mechatronics/equip_add.html'

        self.url_add = reverse('mechatronics:add_equip')
        data = {'submitFolio': 'Buscar', 'folioQuery': '1'}
        self.response = self.client.post(self.url_add, data)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_form_equip_dict(self):
        form_equip = self.response.context['formEquip']
        self.assertEqual(form_equip['folio'].value(), '1')
        self.assertEqual(form_equip.instance.folio, '1')

    def test_template_used(self):
        self.assertTemplateUsed(self.response, self.template_name)

    def test_error_dict(self):
        self.assertTrue('error' in self.response.context)
        self.assertEqual(self.response.context['error'], {})


class EquipAddViewTestPostSearchNoFounded(TestCase):
    '''
    When search a equip by folio and is not founded.
    Ensure a non-existant PK throws a Not Found.
    '''
    fixtures = ['initial_data.json']

    def setUp(self):
        self.template_name = 'mechatronics/equip_add.html'

        self.url_add = reverse('mechatronics:add_equip')
        data = {'submitFolio': 'Buscar', 'folioQuery': '111'}
        self.response = self.client.post(self.url_add, data)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_form_equip_dict(self):
        form_equip = self.response.context['formEquip']
        self.assertEqual(form_equip['folio'].value(), None)
        self.assertEqual(form_equip.instance.folio, '')

    def test_template_used(self):
        self.assertTemplateUsed(self.response, self.template_name)

    def test_error_dict(self):
        self.assertTrue('error' in self.response.context)
        error = {'search': "Folio: 111 dosen't exist"}
        self.assertEqual(self.response.context['error'], error)


# ******************   Test to search equipment view   ******************
class EquipSeachViewTestPostSearchFounded(TestCase):
    '''
    When we have searched a equipment and is founded.
    '''
    fixtures = ['initial_data.json']

    def setUp(self):
        self.template_name = 'mechatronics/equip_search.html'
        self.url_search = reverse('mechatronics:search_equip')

    def test_search_by_date_range_and_status(self):
        data = {
            'date1': '01/01/2015',
            'date2': '01/12/2015',
            'status': 'almacenado'
        }
        response = self.client.get(self.url_search, data)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['equipList']), 10)
        self.assertTemplateUsed(response, self.template_name)
        self.assertFalse('error' in response.context)

    def test_search_by_date_range_and_status_page_2(self):
        data = {
            'submitSearch': 'Buscar',
            'page': 2,
            'date1': '01/01/2015',
            'date2': '01/12/2015',
            'status': 'almacenado',
        }
        response = self.client.get(self.url_search, data)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['equipList']), 1)
        self.assertTemplateUsed(response, self.template_name)
        self.assertFalse('error' in response.context)

    def test_search_by_date_range(self):
        data = {
            'date1': '01/01/2015',
            'date2': '01/12/2015',
            'status': ''
        }
        response = self.client.get(self.url_search, data)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['equipList']), 10)
        self.assertTemplateUsed(response, self.template_name)
        self.assertFalse('error' in response.context)

    def test_search_by_status(self):
        data = {
            'date1': '',
            'date2': '',
            'status': 'almacenado'
        }
        response = self.client.get(self.url_search, data)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['equipList']), 10)
        self.assertTemplateUsed(response, self.template_name)
        self.assertFalse('error' in response.context)


class EquipSeachViewTestPostSearchNoFounded(TestCase):
    '''
    When we have searched a equipment and is not founded.
    '''

    def setUp(self):
        self.template_name = 'mechatronics/equip_search.html'
        self.url_search = reverse('mechatronics:search_equip')

    def test_search_by_date_range_without_objects_in_the_database(self):

        data = {
            'date1': '01/01/2015',
            'date2': '01/06/2015',
            'status': 'almacenado'
        }
        response = self.client.get(self.url_search, data)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['equipList']), 0)
        self.assertTemplateUsed(response, self.template_name)
        self.assertFalse('error' in response.context)

    def test_search_by_status_without_objects_in_the_database(self):
        status_choices = ('diagnosticado', 'reparado',
                          'entregado', 'inreparable',)
        data = {
            'date1': '01/01/2015',
            'date2': '01/12/2015',
        }
        for status in status_choices:
            data['status'] = status
            response = self.client.get(self.url_search, data)

            self.assertEqual(response.status_code, 200)

            self.assertEqual(len(response.context['equipList']), 0)
            self.assertTemplateUsed(response, self.template_name)
            self.assertFalse('error' in response.context)


# *******************   Test to dedi equipment view   *******************
class EquipSeachViewTestPostEdit(TestCase):
    '''
    When we have edited a equipment.
    '''
    fixtures = ['initial_data.json']

    def setUp(self):
        self.template_name = 'mechatronics/equip.edit.html'

    def test_edit_get_search_by_id(self):
        # search by id
        id_1 = Equipo.objects.get(folio=1).id
        url_edit = reverse('mechatronics:edit_equip', args=(id_1,))

        data = {'page': '1', 'date1': '', 'date2': '', 'status': 'almacenado'}
        response = self.client.get(url_edit, data)

        self.assertEqual(response.status_code, 200)

        cxt = response.context
        self.assertEqual(cxt['page'], '1')
        self.assertTrue(not cxt['query']['date1'])
        self.assertTrue(not cxt['query']['date2'])
        self.assertTrue('formEquip' in cxt)
        self.assertEqual(cxt['formEquip']['folio'].value(), '1')
        self.assertEqual(cxt['formEquip'].instance.folio, '1')
        self.assertTemplateUsed(self.template_name)
        self.assertFalse('error' in cxt)

    def test_edit_post_unfollow(self):
        # save the changes in the equip form
        data = {
            "folio": "100", "registro": '2', "estatus": "irreparable",
            "tipo": "edit", "empleado": '1', "marca": "edit",
            "servicios": [1, 2], "entrega": "2015-12-31", "modelo": "edit",
            "total": 800.0, "cliente": '1', 'page': '1',
            'date1': '01/01/2015', 'date2': '01/12/2015', 'status': ''}

        id_1 = Equipo.objects.get(folio=1).id
        url_edit = reverse('mechatronics:edit_equip', args=(id_1,))

        response = self.client.post(url_edit, data)

        self.assertTemplateUsed(self.template_name)
        self.assertEqual(response.status_code, 302)

        cxt = response.context
        self.assertTrue(not cxt)

        equip = Equipo.objects.get(folio=100)

        self.assertEqual(equip.estatus, 'irreparable')
        self.assertTemplateUsed(self.template_name)

    def test_edit_post_follow(self):
        # save the changes in the equip form
        data = {
            "folio": "100", "registro": '2', "estatus": "irreparable",
            "tipo": "edit", "empleado": '1', "marca": "edit",
            "servicios": [1, 2], "entrega": "2015-12-31", "modelo": "edit",
            "total": 800.0, "cliente": '1', 'page': '1',
            'date1': '01/01/2015', 'date2': '01/12/2015', 'status': ''}

        id_1 = Equipo.objects.get(folio=1).id
        url_edit = reverse('mechatronics:edit_equip', args=(id_1,))

        response = self.client.post(url_edit, data, follow=True)

        self.assertTemplateUsed(self.template_name)
        self.assertEqual(response.status_code, 200)

        cxt = response.context
        self.assertEqual(cxt['query']['page'], '1')
        self.assertEqual(cxt['query']['date1'], '01/01/2015')
        self.assertEqual(cxt['query']['date2'], '01/12/2015')
        self.assertTrue(not cxt['query']['status'])

        self.assertFalse('formEquip' in cxt)

        equip = Equipo.objects.get(folio=100)

        self.assertEqual(equip.estatus, 'irreparable')
        self.assertTemplateUsed(self.template_name)


# ******************   Test to delete equipment view   ******************
class EquipSeachViewTestPostDelete(TestCase):
    '''
    When we have deleted a equipment.
    '''
    fixtures = ['initial_data.json']

    def setUp(self):
        # self.template_name = 'mechatronics/equip_delete.html'
        self.url_delete = reverse('mechatronics:delete_equip')

    def test_delete(self):
        id_1 = Equipo.objects.get(folio='1').id
        id_2 = Equipo.objects.get(folio='2').id
        data = {'delete': [id_1, id_2], 'page': '',
                'date1': '', 'date2': '', 'status': ''}

        self.assertEqual(Equipo.objects.count(), 11)

        response = self.client.post(self.url_delete, data=data)
        self.assertEqual(Equipo.objects.count(), 9)
        self.assertEqual(response.status_code, 302)

    def test_delet_follow_true(self):
        id_1 = Equipo.objects.get(folio='1').id
        id_2 = Equipo.objects.get(folio='2').id
        data = {'delete': [id_1, id_2], 'page': '',
                'date1': '01/01/2015', 'date2': '01/12/2015', 'status': ''}

        self.assertEqual(Equipo.objects.count(), 11)

        response = self.client.post(self.url_delete, data, follow=True)
        self.assertEqual(Equipo.objects.count(), 9)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context['equipList']), 9)
        self.assertTemplateUsed(response, 'mechatronics/equip_search.html')

        self.assertTrue('query' in response.context)
        self.assertEqual(response.context['query']['date1'], '01/01/2015')
        self.assertEqual(response.context['query']['date2'], '01/12/2015')
        self.assertEqual(response.context['query']['status'], '')
        self.assertFalse('error' in response.context)
