from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from forms import DelayRepayUserRegForm, LoginForm


def register_success(request):
    return render_to_response('register_success.html')


def register_user(request):
    args = {}
    args.update(csrf(request))

    if request.method == 'POST':
        form = DelayRepayUserRegForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/register_success')
        else:
            args['form'] = form
            return render_to_response('register.html', args)

    else:
        args['form'] = DelayRepayUserRegForm()
        return render_to_response('register.html', args)


def index(request):
    return HttpResponse("This is the main index page")


def login(request):
    c = {}
    c.update(csrf(request))
    c['form'] = LoginForm()
    return render_to_response('login.html', c)


def auth_view(request):
    if 'login' in request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return HttpResponseRedirect('/accounts/loggedin')
        else:
            return HttpResponseRedirect('/accounts/invalid')
    else:
        return HttpResponseRedirect('/accounts/register')


def loggedin(request):
    if request.user.is_authenticated():
        return render_to_response('loggedin.html',
            {'full_name': request.user.username}
        )
    else:
        return HttpResponseRedirect('/accounts/login')

def invalid_login(request):
    return render_to_response('invalid_login.html')

def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')