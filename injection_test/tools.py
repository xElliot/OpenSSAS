import re
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
        result = str
    else:
        result = 'wrong injection_url'
    return result