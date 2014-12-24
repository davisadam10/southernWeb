# coding=utf-8
"""
Views for the delay repay app
"""
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
import forms as delayRepayForms


def register_success(request):
    """

    :param request:
    :return: :rtype:
    """
    return render_to_response('register_success.html')


def register_user(request):
    """

    :param request:
    :return: :rtype:
    """
    args = {}
    args.update(csrf(request))

    if request.method == 'POST':
        form = delayRepayForms.DelayRepayUserRegForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/register_success')
        else:
            args['form'] = form
            return render_to_response('register.html', args)

    else:
        args['form'] = delayRepayForms.DelayRepayUserRegForm()
        return render_to_response('register.html', args)


def index(request):
    """

    :param request:
    :return: :rtype:
    """
    return HttpResponse("This is the main index page")


def login(request):
    """

    :param request:
    :return: :rtype:
    """
    c = {}
    c.update(csrf(request))
    c['form'] = delayRepayForms.LoginForm()
    return render_to_response('login.html', c)


def auth_view(request):
    """

    :param request:
    :return: :rtype:
    """
    if 'login' in request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/logged_in')
        else:
            return HttpResponseRedirect('/invalid')
    else:
        return HttpResponseRedirect('/register')


def addJourney(request):
    """

    :param request:
    :return: :rtype:
    """
    args = {}
    args.update(csrf(request))
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = delayRepayForms.JourneyForm(request.POST)
            if form.is_valid():
                form.save(user=request.user)
                return HttpResponseRedirect('/register_success')
            else:
                args['form'] = form
                return render_to_response('addJourney.html', args)

        else:
            args['form'] = delayRepayForms.JourneyForm()
            return render_to_response('addJourney.html', args)
    else:
        return HttpResponseRedirect('/login')


def addTicket(request):
    """

    :param request:
    :return: :rtype:
    """
    args = {}
    if request.user.is_authenticated():
        args['form'] = delayRepayForms.TicketForm()
        return render_to_response('addTicket.html', args)
    else:
        return HttpResponseRedirect('/login')


def logged_in(request):
    """

    :param request:
    :return: :rtype:
    """
    args = {}
    if request.user.is_authenticated():
        args['form'] = delayRepayForms.JourneyForm()
        return render_to_response('logged_in.html', args)
    else:
        return HttpResponseRedirect('/login')


def invalid_login(request):
    """

    :param request:
    :return: :rtype:
    """
    return render_to_response('invalid_login.html')


def logout(request):
    """

    :param request:
    :return: :rtype:
    """
    auth.logout(request)
    return render_to_response('logout.html')