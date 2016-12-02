# -*- coding:utf-8 -*-
import re
from http import cookiejar
from urllib import request, parse

__author__ = 'Elliot'


def get_home(str):
    list = str.split('/')
    return list[0]


def get_scan_name(str):
    return 'new task(' + str + ')'


# page_name = http://python.jobbole.com/tag/pyquery/
# page_name = https://hao123.com

def get_i_url(str, page_name):
    str = str.split('?')[0]
    result = ''
    if str.startswith('//'):
        result = 'http:' + str
    elif str.startswith('/'):
        page_name_list = page_name.split('.')
        page_name_list2 = page_name_list[-1].split('/')
        for i in range(0, len(page_name_list)-1):
            page_name_list[i] += '.'
            result += page_name_list[i]
        result += page_name_list2[0]
        result += str
    elif str.startswith('http'):
        # 如果链接不需要补充完整处理，检查是否和域名相同
        page_name_list = page_name.split('.')
        a_href_list = str.split('.')
        if page_name_list[1] == a_href_list[1]:
            result = str
        else:
            result = None
    else:
        result = None
    return result


def inject_check(i_object):
    pass


'''
使用GET方法发送请求
'''
def request_get(url, i, parameter_name, parameter_value):
    i_query = '?'
    for j in range(len(parameter_name)):
        if i == j:
            i_query += parameter_name[j] + '=' + "'" + '&'
        else:
            i_query += parameter_name[j] + '=' + parameter_value[j] + '&'
    i_query = i_query[0:-1]

    data = request.urlopen(url + i_query).read().decode()
    if '<pre>You have an error in your SQL syntax; check the manual that corresponds to your MySQL server ' \
       'version for the right syntax to use near' in data:
        return 'MySQL'
    elif "Server Error in '/' Application" in data:
        return 'Microsoft SQL Server'
    elif 'ORA-' in data:
        return 'Oracle'
    elif 'Query failed:' in data:
        return 'PostgreSQL'
    else:
        return False


def request_post():
    pass

'''
检查一个参数是不是可注入的
'''
def check_one_parameter(url, i, **kwargs):
    parameter_name = kwargs.get('parameter_name', '')
    parameter_value = kwargs.get('parameter_value', '')
    domain = get_domain_from_url(url)

    i_query = '?'
    for j in range(len(parameter_name)):
        if i == j:
            i_query += parameter_name[j] + '=' + "'" + '&'
        else:
            i_query += parameter_name[j] + '=' + parameter_value[j] + '&'
    i_query = i_query[0:-1]

    if 'cookies' in kwargs:
        cookies = kwargs.get('cookies')
        opener = make_opener_with_cookie(cookies, domain)
        try:
            data = opener.open(url + i_query).read().decode()
        except UnicodeDecodeError as e:
            data = opener.open(url + i_query).read().decode('gbk2312')
    else:
        try:
            data = request.urlopen(url + i_query).read().decode()
        except UnicodeDecodeError as e:
            # data = request.urlopen(url + i_query).read().decode('gbk2312')
            data = ''
    if '<pre>You have an error in your SQL syntax; check the manual that corresponds to your MySQL server ' \
       'version for the right syntax to use near' in data:
        return 'MySQL'
    elif "Server Error in '/' Application" in data:
        return 'Microsoft SQL Server'
    elif 'ORA-' in data:
        return 'Oracle'
    elif 'Query failed:' in data:
        return 'PostgreSQL'
    else:
        return False

'''
返回http状态码
'''
def check_http_status(i_open):
    status = i_open.status

'''
制作自己的cookie，用于产生cookie
'''
def make_cookie(name, value, domain):
    return cookiejar.Cookie(
        version=0,
        name=name,
        value=value,
        port=None,
        port_specified=False,
        domain=domain,
        domain_specified=True,
        domain_initial_dot=False,
        path="/",
        path_specified=True,
        secure=False,
        expires=None,
        discard=False,
        comment=None,
        comment_url=None,
        rest=None
    )


def set_value(i_parameters):
    para_name = []
    para_value = []
    for i_parameter in i_parameters:
        value = i_parameter.i_value
        if value is '':
            imaginary_value = ''
            para_value.append(imaginary_value)
        else:
            para_value.append(i_parameter.i_value)
        para_name.append(i_parameter.name)

    return para_name, para_value


'''
处理用户提交的cookie，除去分号
'''
def correct_cookie(str):
    cookie_result = []
    cookie_list = str.split(';')
    for cookie in cookie_list:
        cookie_demo = cookie.split('=')
        cookie_result.append((cookie_demo[0], cookie_demo[1]))
    return cookie_result


'''
使用cookie制作一个opener
'''


def make_opener_with_cookie(cookies, domain):
    cj = cookiejar.MozillaCookieJar()
    for cookie in cookies:
        cj.set_cookie(make_cookie(cookie[0], cookie[-1]), domain)
    handler = request.HTTPCookieProcessor(cj)
    opener = request.build_opener(handler)
    return opener


'''
获取网站的domain
'''


def get_domain_from_url(site_url):
    if 'https://' in site_url:
        pass
    elif 'http://' in site_url:
        pass
    else:
        site_url = 'http://' + site_url
    final_url = parse.urlparse(site_url)
    url_data_list = parse.parse_qsl(final_url.query)
    domain0 = '{uri.scheme}://{uri.netloc}'.format(uri=final_url)
    domain1 = '{uri.scheme}://{uri.netloc}{uri.path}'.format(uri=final_url)
    domain = domain0.replace('https://', '').replace('http://', '').replace('www.', '').replace('/', '')
    return domain