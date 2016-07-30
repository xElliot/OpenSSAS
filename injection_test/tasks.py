__author__ = 'Elliot'

from celery import task
from pyquery import PyQuery as pq
from .models import *


@task
def add(x, y):
    return x + y


@task
def i_scan(task):
    # page_name = 'download.html'
    # page_name = 'http://python.jobbole.com/85222/'
    # page_name = 'https://www.hao123.com'
    page_name = task.page

    html = pq(page_name)
    h_a = html('a')
    if h_a:

        i = 0
        for a in h_a.items():
            i += 1
            a_href = a.attr('href')
            if a_href:
                # print(str(i) + '-' + a_href)
                i_object = IObject.objects.create(task=task)
                i_object.i_url = get_i_url(a_href, page_name)
                i_object.save()
                i_parameter_list = a_href.split('?')
                if len(i_parameter_list) > 1:
                    i_parameter_list_object_list = i_parameter_list[-1].split('&')
                    for i_parameter_list_object in i_parameter_list_object_list:
                        i_parameter = IParameter.objects.create(i_object=i_object)
                        i_parameter_entity = i_parameter_list_object.split('=')
                        i_parameter.name = i_parameter_entity[0]
                        if len(i_parameter_entity) > 1:
                            i_parameter.i_value = i_parameter_entity[1]
                        else:
                            i_parameter.i_value = ''
                        i_parameter.save()
            # else:
                # print(str(i) + '-NONE' )
    # print('-------------------------')

    h_form_list = html('form')
    if h_form_list:
        for h_form in h_form_list.items():
            i_object = IObject.objects.create(task=task)
            h_form_action = h_form.attr('action')
            h_form_method = h_form.attr('method')
            if h_form_method == 'post':
                i_object.i_method = 2
                i_object.save()
            if h_form_action:
                i_object.i_url = get_i_url(h_form_action, page_name)
                i_object.save()
                # print(h_form_action)
                # print(h_form.text())
                h_form_action_input_list = h_form.find('input')
                h_form_action_textarea_list = h_form.find('textarea')
                h_form_action_option_list = h_form.find('option')
                if h_form_action_option_list:
                    for h_form_action_option in h_form_action_option_list.items():
                        i_url = get_i_url(h_form_action_option, page_name)
                        i_o = IObject.objects.get_or_create(task=task, i_url=i_url)
                        if h_form_action_input_list:
                            for h_form_action_input in h_form_action_input_list.items():
                                name = h_form_action_input.attr('name')
                                id = h_form_action_input.attr('id')
                                value = h_form_action_input.attr('value')
                                i_parameter = IParameter.objects.create(i_object=i_o)
                                if name:
                                    i_parameter.name = name
                                elif id:
                                    i_parameter.name = id
                                else:
                                    i_parameter.name = 'no name'
                                if value:
                                    i_parameter.i_value = value
                                else:
                                    i_parameter.i_value = ''
                                i_parameter.save()
                        if h_form_action_textarea_list:
                            for h_form_action_textarea in h_form_action_textarea_list.items():
                                name = h_form_action_textarea.attr('name')
                                id = h_form_action_textarea.attr('id')
                                value = h_form_action_textarea.attr('value')
                                i_parameter = IParameter.objects.create(i_object=i_o)
                                if name:
                                    i_parameter.name = name
                                elif id:
                                    i_parameter.name = id
                                else:
                                    i_parameter.name = 'no name'
                                if value:
                                    i_parameter.i_value = value
                                else:
                                    i_parameter.i_value = ''
                                i_parameter.save()
                else:
                    if h_form_action_input_list:
                        for h_form_action_input in h_form_action_input_list.items():
                            # print(h_form_action_input)
                            name = h_form_action_input.attr('name')
                            id = h_form_action_input.attr('id')
                            value = h_form_action_input.attr('value')
                            i_parameter = IParameter.objects.create(i_object=i_object)
                            if name:
                                i_parameter.name = name
                            elif id:
                                i_parameter.name = id
                            else:
                                i_parameter.name = 'no name'
                            if value:
                                i_parameter.i_value = value
                            else:
                                i_parameter.i_value = ''
                            i_parameter.save()
                    if h_form_action_textarea_list:
                        for h_form_action_textarea in h_form_action_textarea_list.items():
                            name = h_form_action_textarea.attr('name')
                            id = h_form_action_textarea.attr('id')
                            value = h_form_action_textarea.attr('value')
                            i_parameter = IParameter.objects.create(i_object=i_object)
                            if name:
                                i_parameter.name = name
                            elif id:
                                i_parameter.name = id
                            else:
                                i_parameter.name = 'no name'
                            if value:
                                i_parameter.i_value = value
                            else:
                                i_parameter.i_value = ''
                            i_parameter.save()
            # print('form------------------------')
    return