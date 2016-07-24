import warnings

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.utils.http import is_safe_url
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model, \
    REDIRECT_FIELD_NAME
from django.contrib.auth.views import login as LOGIN
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import deprecate_current_app
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, render_to_response, resolve_url
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)

# Create your views here.
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.utils.deprecation import RemovedInDjango110Warning
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from OpenSSAS import settings
from injection_test.forms import LoginForm
from .models import *


def index(request):
    return HttpResponse("hello world. You are at the index.")


def login1(request,
           template_name='injection_test/index.html'):
    if request.method == 'GET':
        form = LoginForm()
        return render_to_response('injection_test/login2.html',
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
