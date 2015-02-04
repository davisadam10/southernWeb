# coding=utf-8
"""
Views for the delay repay app
"""
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.core.context_processors import csrf
import forms as delayRepayForms
import delayRepay.models as models
import delayRepay.utils as utils


def register_success(request):
    """

    :param request:
    :return: :rtype:
    """
    return HttpResponseRedirect('/')


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
            return HttpResponseRedirect('/')
        else:
            args['form'] = form
            return render_to_response('register.html', args)

    else:
        args['form'] = delayRepayForms.DelayRepayUserRegForm()
        return render_to_response('register.html', args)


def login(request):
    """

    :param request:
    :return: :rtype:
    """
    args = {}
    args.update(csrf(request))
    if 'login' in request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            form = delayRepayForms.LoginForm(request.POST)
            args['form'] = form
            return render_to_response('login.html', args)

    elif 'register' in request.POST:
        return HttpResponseRedirect('/register')

    else:
        args['form'] = delayRepayForms.LoginForm()
        return render_to_response('login.html', args)


def index(request):
    """

    :param request:
    :return: :rtype:
    """
    args = {}
    args.update(csrf(request))
    if request.user.is_authenticated():
        user_model = utils.get_user_model_from_request(request)
        if not user_model:
            return HttpResponseRedirect('/login')

        args['journeys'] = utils.get_user_journeys(user_model)
        journey_names = ["#journeyItem%s" % journey.id for journey in args['journeys']]
        args['journey_names'] = ', '.join(journey_names)

        if request.method == 'POST':
            journey = [journey for journey in args['journeys'] if journey.id == int(request.POST['journey_name'])]
            form = delayRepayForms.DelayForm(request.POST)
            if form.is_valid():
                delay = form.save(user=request.user, journey=journey[0])
                success = utils.submit_delay(request, delay, journey[0])
                if not success:
                    delay.delete()
                    return HttpResponseRedirect('/noTicket')

                delay.claimed = True
                delay.save()
                friends = user_model.friends.all()
                for friend in friends:
                    delay.claimed = False
                    delay.pk = None
                    delay.delayRepayUser = friend
                    delay.save()

                return HttpResponseRedirect('/delaySuccess')
            else:
                args['form'] = form
                return render_to_response('index.html', args)
        else:
            args['form'] = delayRepayForms.DelayForm()
            return render_to_response('index.html', args)
    else:
        return HttpResponseRedirect('/login')



def addJourney(request):
    """

    :param request:
    :return: :rtype:
    """
    args = {}
    args.update(csrf(request))
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = delayRepayForms.JourneyForm(request.POST, request=request)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/')
            else:
                args['form'] = form
                return render_to_response('addJourney.html', args)

        else:
            args['form'] = delayRepayForms.JourneyForm(request=request)
            return render_to_response('addJourney.html', args)
    else:
        return HttpResponseRedirect('/login')


def addTicket(request):
    """

    :param request:
    :return: :rtype:
    """
    args = {}
    args.update(csrf(request))
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = delayRepayForms.TicketForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(user=request.user)
                return HttpResponseRedirect('/')
            else:
                args['form'] = form
                return render_to_response('addTicket.html', args)
        else:
            args['form'] = delayRepayForms.TicketForm()
            return render_to_response('addTicket.html', args)
    else:
        return HttpResponseRedirect('/login')


def addFriend(request):
    """

    :param request:
    :return: :rtype:
    """
    args = {}
    args['friends'] = []
    args.update(csrf(request))
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = delayRepayForms.FriendForm(request.POST, request=request)
            if form.is_valid():
                user_model = utils.get_user_model_from_request(request)
                cleaned_data = form.clean()
                user_model.friends.add(cleaned_data['friend_model'])
                user_model.save()
                args['friends'] = [friend.username for friend in user_model.friends.all()]
                args['form'] = delayRepayForms.FriendForm()
                return render_to_response('addFriend.html', args)
            else:
                args['form'] = form
                return render_to_response('addFriend.html', args)
        else:
            args['form'] = delayRepayForms.FriendForm()
            return render_to_response('addFriend.html', args)
    else:
        return HttpResponseRedirect('/login')


def noTicket(request):
    args = {}
    args.update(csrf(request))
    if request.user.is_authenticated():
        return render_to_response('noTicket.html', args)
    else:
        return HttpResponseRedirect('/')

def delaySuccess(request):
    args = {}
    args.update(csrf(request))
    if request.user.is_authenticated():
        return render_to_response('delaySuccess.html', args)
    else:
        return HttpResponseRedirect('/')

def logged_in(request):
    """

    :param request:
    :return: :rtype:
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
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
    return HttpResponseRedirect('/')