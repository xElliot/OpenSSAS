# -*- coding:utf8 -*-
__author__ = 'Elliot'

from celery import task
from pyquery import PyQuery as pq
from .models import *
from urllib import parse, request, error
from .tools import check_one_parameter

@task
def add(x, y):
    return x + y


@task
def i_scan(task, **kwargs):
    # page_name = 'download.html'
    page_name = task.page
    domain = get_domain_from_url(page_name)
    if 'cookies' in kwargs:
        cookies = kwargs.get('cookies')
        opener = make_opener_with_cookie(cookies ,domain)
        response = opener.open(page_name)
        html = pq(response.read())
    else:
        html = pq(page_name)
    h_a = html('a')
    if h_a:

        i = 0
        for a in h_a.items():
            i += 1
            a_href = a.attr('href')
            if a_href:
                i_url = get_i_url(a_href, page_name)
                i_parameter_list = a_href.split('?')
                i_parameter_list_object_list = i_parameter_list[-1].split('&')
                if len(i_parameter_list) > 1:
                    if i_url:
                        i_object_list = IObject.objects.filter(task=task, i_url=i_url)
                        num = i_object_list.count()
                        if num > 1:
                            # 去除重复设置-如果i_url相同数目大于1，删除num-1个数据
                            for i in range(1, num):
                                i_object_list[i].delete()
                        elif num == 0:
                            # 去除重复设置-如果没有重复
                            i_object = IObject.objects.create(task=task, i_url=i_url)
                            for i_parameter_list_object in i_parameter_list_object_list:
                                i_parameter = IParameter.objects.create(i_object=i_object)
                                i_parameter_entity = i_parameter_list_object.split('=')
                                i_parameter.name = i_parameter_entity[0]
                                if len(i_parameter_entity) > 1:
                                    i_parameter.i_value = i_parameter_entity[1]
                                else:
                                    i_parameter.i_value = ''
                                i_parameter.save()
                        else:
                            name_set = set()
                            name_set2 = set()
                            name = ''
                            # 去除重复设置-如果存在i_url相同，比较参数值
                            db_i_parameter_list = i_object_list[0].i_parameters.all()
                            for single_object in db_i_parameter_list:
                                name_set.add(single_object.name)
                            for i_parameter_list_object in i_parameter_list_object_list:
                                name = i_parameter_list_object.split('=')[0]
                                name_set2.add(name)

                            if name_set == name_set2:
                                pass
                            else:
                                i_object = IObject.objects.create(task=task, i_url=i_url)
                                for i_parameter_list_object in i_parameter_list_object_list:
                                    i_parameter = IParameter.objects.create(i_object=i_object)
                                    i_parameter_entity = i_parameter_list_object.split('=')
                                    i_parameter.name = i_parameter_entity[0]
                                    if len(i_parameter_entity) > 1:
                                        i_parameter.i_value = i_parameter_entity[1]
                                    else:
                                        i_parameter.i_value = ''
                                    i_parameter.save()

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
                i_url = get_i_url(h_form_action, page_name)
                if i_url:
                    i_object.i_url = i_url
                    i_object.save()
                    h_form_action_input_list = h_form.find('input')
                    h_form_action_textarea_list = h_form.find('textarea')
                    h_form_action_option_list = h_form.find('option')
                    if h_form_action_option_list:
                        for h_form_action_option in h_form_action_option_list.items():
                            i_url = get_i_url(h_form_action_option.attr('value'), page_name)
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


@task
def i_get(i_object, **kwargs):
    try:
        # site = 'http://www.hao123.com'
        site = i_object.i_url
        if 'https://' in site:
            pass
        elif 'http://' in site:
            pass
        else:
            site = 'http://' + site
        final_url = parse.urlparse(site)
        url_data_list = parse.parse_qsl(final_url.query)
        domain0 = '{uri.scheme}://{uri.netloc}'.format(uri=final_url)
        domain1 = '{uri.scheme}://{uri.netloc}{uri.path}'.format(uri=final_url)
        domain = domain0.replace('https://', '').replace('http://', '').replace('www.', '').replace('/', '')
        connection = request.urlopen(domain0, timeout=20)
        url = site
        i_parameters = i_object.i_parameters.all()
        para_name = []
        para_value = []
        report = []
        para_name, para_value = set_value(i_parameters)
        for i in range(0, len(para_name)):
            if 'cookies' in kwargs:
                cookies = kwargs.get('cookies')
                result = check_one_parameter(domain1, i, parameter_name=para_name, parameter_value=para_value, cookies=cookies)
            else:
                result = check_one_parameter(domain1, i, parameter_name=para_name, parameter_value=para_value, )
            if result:
                return 'Parameter \"' + para_name[i] + '\" is vulnerable! The dbms is ' + result + '.'
            else:
                report.append('Parameter \"' + para_name[i] + '\" maybe not vulnerable.')
        return report
    except error.URLError as e:
        return 'Error: Site \"' + domain + '\" is offline!'