import string
import random
import time

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from user.forms import LoginForm,RegForm,ChangeNicknameForm,BindEmailForm,ChangePasswordForm,Forgot_PasswordForm
from .models import Profile
from django.core.mail import  send_mail

# Create your views here.
# 登录检测
def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect( reverse('home'))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'templates_user/login.html', context)



# 创建用户和登录
def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST,request=request)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password_again']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            #清楚session
            del request.session['register_code']
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'templates_user/register.html', context)

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))

#个人中心
def user_info(request):
    context = {}
    return render(request, 'templates_user/user_info.html', context)

#修改昵称
def change_nickname(request):
    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST,user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile,created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(request.GET.get('from',reverse('home')))
    else:
        form = ChangeNicknameForm()
    context = {}
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['return_back_url'] = request.GET.get('from',reverse('home'))
    context['form'] = form
    return render(request,'form.html',context)

#绑定邮箱
def bind_email(request):
    if request.method == 'POST':
        form = BindEmailForm(request.POST,request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            # 清楚session
            del request.session['bind_email_code']
            return redirect(request.GET.get('from',reverse('home')))

    else:
        form = BindEmailForm()
    context = {}
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['return_back_url'] = request.GET.get('from',reverse('home'))
    context['form'] = form
    return render(request,'templates_user/bind_email.html',context)

#发送验证码
def send_verification_code(request):
    email = request.GET.get('email','')
    send_for = request.GET.get('send_for','')
    data = {}
    if email != '':
        #生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits,4))
        now = int(time.time())
        send_time_code = request.session.get('send_time_code',0)
        if now - send_time_code < 30 :
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code

            request.session['send_time_code'] = now
        send_mail(
            '绑定邮箱',
            '验证码: %s' % code,
            '893438873@qq.com',
            [email],
            fail_silently=False,
        )
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

#修改密码
def change_password(request):
    redirect_to = reverse('home')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST,user=request.user)
        if form.is_valid():
            user = request.user
            new_passwrod = form.cleaned_data['new_password']
            user.set_password(new_passwrod)
            user.save()
            auth.login(request, user)
            return redirect(redirect_to)
    else:
        form = ChangePasswordForm()
    context = {}
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['return_back_url'] = redirect_to
    context['form'] = form
    return render(request,'form.html',context)

#忘记密码
def forgot_password(request):
    redirect_to = reverse('home')
    if request.method == 'POST':
        form = Forgot_PasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            # 清楚session
            del request.session['forgot_password_code']
            return redirect(redirect_to)

    else:
        form = Forgot_PasswordForm()
    context = {}
    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '重置'
    context['return_back_url'] = request.GET.get('from', reverse('home'))
    context['form'] = form
    return render(request, 'templates_user/forgot_password.html', context)
