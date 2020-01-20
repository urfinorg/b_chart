from django.shortcuts import render, redirect
from django.middleware import csrf

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect

from .forms import *
from .models import *

import datetime
import json

def home(request):
    now_time = datetime.datetime.now()

    page_context = { 'now_time': now_time,
                    'login_form' : AuthenticationForm(),  #LoginForm()
                    'reg_form': RegistrationForm()}  #UserCreationForm()

    return render( request, 'index_page.html', context = page_context)

def api(request):
    form_id = request.POST.get('form_id')
    response_data = {'err_code': 1, 'msg': 'wrong way... can`t find form_id'}

    if form_id == 'reg_form':
        response_data = ajax_try_registration(request)

    elif form_id == 'login_form':
        response_data = ajax_try_login(request)

    elif form_id == 'logout':
        logout(request)
        response_data = {'err_code':0, 'msg':'logout success'}

    elif form_id == 'message_form':
        response_data = ajax_receive_message(request)

    elif form_id == 'get_message':
        response_data = ajax_get_message(request)

    return HttpResponse(json.dumps(response_data), content_type="application/json")


def ajax_get_message(request):
    response_data = {}
    last_message_id = request.POST.get('msg')
    if last_message_id is None:
        last_message_id = -1

    chat_message = ChatMessage.objects.latest('created')

    if (chat_message is not None):
        response_data['err_code'] = 0
        response_data['msg'] = chat_message.msg
        response_data['username'] = chat_message.user.username
        response_data['message_id'] = chat_message.id
    else:
        response_data['err_code'] = 0
        response_data['msg'] = 'No messages yet.'
        response_data['username'] = 'system'
        response_data['message_id'] = 0

    return response_data

def ajax_receive_message(request):
    response_data = {}
    if request.user.is_authenticated:
        response_data['err_code'] = 0
        message = request.POST.get('msg')

        if (message is not None) & (message != ''):
            chat_message = ChatMessage()
            chat_message.msg = message
            chat_message.user = request.user
            chat_message.save()

            print('%s Receive message from %s: %s' % (datetime.datetime.now(), request.user.username, message))
            #save to file
    else:
        response_data['err_code'] = 1
        response_data['msg'] = 'you need to be login in, before you can send message'

    return response_data



## Наткнулся на странный баг при попытке унаследоваться от UserCreationForm
## пароли просто не совпадают
## https://stackoverflow.com/questions/54962040/password-mismatch-in-registration-form-that-inherits-from-usercreationform
## https://stackoverflow.com/questions/56760195/built-in-usercreationform-throws-the-two-password-fields-didnt-match-when-pas
## в качестве супер быстрого решения заглушил is_valid

def ajax_try_registration(request):
    response_data = {}
    form = RegistrationForm(request.POST)

    if form.is_valid():
        #user = form.save()
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')

        user = User.objects.create_user(username, email, password)
        #user.save()
        login(request, user)
        response_data['err_code'] = 0
        response_data['msg'] = 'created user success %s  %s  %s ' % (username, email, password)
        response_data['username'] = username
        response_data['csrf'] = csrf.get_token(request)
        return response_data
    else:
        response_data['err_code'] = 1
        str_err = ''
        for msg in form.error_messages:
            str_err += msg
        response_data['msg'] = str_err

    return response_data

def ajax_try_login(request):
    response_data = {}
    form = AuthenticationForm(request=request, data=request.POST)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            response_data['err_code'] = 0
            response_data['msg'] = 'You are now logged in success'
            response_data['username'] = username
            response_data['csrf'] = csrf.get_token(request)
            return response_data
    else:
        response_data['err_code'] = 1
        response_data['msg'] = 'Invalid username or password'
        return response_data



