# coding=utf-8
"""
Views for the delay repay app
"""
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
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
            if user.is_active:
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
    if request.user.is_authenticated() and request.user.is_active:
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
                already_claimed = [claimed_delay for claimed_delay in utils.get_delays_for_date(user_model, delay.date) if claimed_delay.claimed]
                if already_claimed:
                    delay.delete()
                    return render_to_response('alreadyClaimed.html', {'redirect': '/'})
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
                    if not utils.check_delay_already_found(friend, delay):
                        delay.save()

                return render_to_response('delaySuccess.html', {'redirect': '/'})
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
    if request.user.is_authenticated() and request.user.is_active:
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
    if request.user.is_authenticated() and request.user.is_active:
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
    args = {'friends': []}
    args.update(csrf(request))
    if request.user.is_authenticated() and request.user.is_active:
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
    """

    :param request:
    :type request:
    :return:
    :rtype:
    """
    args = {}
    args.update(csrf(request))
    if request.user.is_authenticated() and request.user.is_active:
        return render_to_response('noTicket.html', args)
    else:
        return HttpResponseRedirect('/')


def logged_in(request):
    """

    :param request:
    :return: :rtype:
    """
    if request.user.is_authenticated() and request.user.is_active:
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


def unclaimedDelays(request):
    """

    :param request:
    :type request:
    :return:
    :rtype:
    """
    args = {}
    args.update(csrf(request))
    if request.user.is_authenticated() and request.user.is_active:
        user_model = utils.get_user_model_from_request(request)
        if request.method == 'POST':
            no_ticket = 'no_ticket' in request.POST.keys()
            remove_ticket = 'remove_ticket' in request.POST.keys()
            if no_ticket or remove_ticket:
                delay_id = request.POST.get('delay_Id')
                delay = models.Delay.objects.filter(id=delay_id)[0]
                delay.delete()
                return HttpResponseRedirect('/unclaimedDelays')

            delay_id = request.POST.get('delay_Id')
            new_delay = models.Delay.objects.filter(id=delay_id)[0]
            already_claimed = [delay for delay in utils.get_delays_for_date(user_model, new_delay.date) if delay.claimed]
            if not already_claimed:
                success = utils.submit_delay(request, new_delay, new_delay.journey)
                if success:
                    new_delay.claimed = True
                    new_delay.save()
                    return render_to_response('delaySuccess.html', {'redirect': '/unclaimedDelays'})

            new_delay.delete()
            return render_to_response('alreadyClaimed.html', {'redirect': '/unclaimedDelays'})

        all_unclaimed = models.Delay.objects.filter(delayRepayUser=user_model, claimed=False)
        args['unclaimed_claimable'] = [
            delay for delay in all_unclaimed if
            utils.get_best_valid_ticket(user_model, delay.date)
        ]
        args['unclaimed_noTicket'] = [
            delay for delay in all_unclaimed if
            not utils.get_best_valid_ticket(user_model, delay.date)
        ]
        return render_to_response('unclaimedDelays.html', args)
    else:
        return HttpResponseRedirect('/')