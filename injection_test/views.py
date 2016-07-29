from django.contrib.auth import (
    REDIRECT_FIELD_NAME, logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import deprecate_current_app
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, HttpResponse, render_to_response, resolve_url
from django.utils.http import is_safe_url
from django.utils.translation import ugettext as _

# Create your views here.
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache

from injection_test.forms import LoginForm
from .models import *
from .tasks import *


@login_required
def injection_object(request,
                     template_name='injection_test/app_index.html',
                     task_id=1):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404('Task does not exist')
    context = {
        'admin_log': True,
        'task': task,
        'has_permission': True,
        'is_login': True,
        'title': _('Injection urls and parameters'),
        'app_list': ['injection_object'],
    }
    return render(request, template_name, context)

# @deprecate_current_app
@login_required
def quick_scan(request,
               template_name='injection_test/index.html'):
    page_name = request.POST.get('page_name', '')
    name = get_scan_name(page_name)
    policy, created = Policy.objects.get_or_create(name='Quick Scan')
    task = Task.objects.create(name=name, page=page_name)
    task.policies.add(policy)
    task_list = Task.objects.all()
    i_scan(task)
    # i_scan.delay(task)
    context = {
        'has_permission': True,
        'is_login': True,
        'task_list': task_list,
        'title': _('Welcome'),
        'admin_log': True,
    }

    return render(request, template_name, context)


def index(request):
    return HttpResponse("hello world. You are at the index.")


def login1(request,
           template_name='injection_test/login2.html'):
    if request.method == 'GET':
        form = LoginForm()
        return render_to_response(template_name,
                                  RequestContext(request, {'form': form}))


# @sensitive_post_parameters
@never_cache
def login_to_index(request,
                   template_name='injection_test/index.html'):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                task_list = Task.objects.all()
                context = {
                    'has_permission': True,
                    'is_login': True,
                    'task_list': task_list,
                    'title': _('Welcome'),
                    'admin_log': True,
                }
                return render(request, template_name, context)
            else:
                return render_to_response('injection_test/login2.html',
                                          RequestContext(request, {'form': form, 'password_is_wrong': True}))
        else:
            return render_to_response('injection_test/login2.html', RequestContext(request, {'form': form,}))


@deprecate_current_app
def logout_from_index(request, next_page=None,
                      template_name='injection_test/logged_out.html',
                      redirect_field_name=REDIRECT_FIELD_NAME,
                      extra_context=None):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    auth_logout(request)

    if next_page is not None:
        next_page = resolve_url(next_page)

    if (redirect_field_name in request.POST or
                redirect_field_name in request.GET):
        next_page = request.POST.get(redirect_field_name,
                                     request.GET.get(redirect_field_name))
        # Security check -- don't allow redirection to a different host.
        if not is_safe_url(url=next_page, host=request.get_host()):
            next_page = request.path

    if next_page:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(next_page)

    current_site = get_current_site(request)
    context = {
        'site': current_site,
        'site_name': current_site.name,
        'title': _('Logged out'),
        'has_permission': False,
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


@login_required
def password_change(request,
                    template_name='registration/password_change_form.html',
                    password_change_form=PasswordChangeForm,
                    extra_context=None):
    if request.method == 'POST':
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect()
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': _('Password change'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context)
