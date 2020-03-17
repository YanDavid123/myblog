import datetime
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_data
from blogapp.models import Blog
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from user.forms import LoginForm
from user.forms import RegForm
from django.http import JsonResponse


# 前七天热门博客排行榜
def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date) \
        .values('id', 'title') \
        .annotate(read_num_sum=Sum('read_details__read_num')) \
        .order_by('-read_num_sum')
    return blogs[:7]


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)

    # 获取7天热门博客的缓存数据
    hot_blog_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blog_for_7_days is None:
        hot_blog_for_7_days = get_7_days_hot_blogs()
        cache.set('hot_blogs_for_7_days', hot_blog_for_7_days, 3600)
        print('cache')
    else:
        print('use cache')

    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums

    context['hot_blogs_for_7_days'] = hot_blog_for_7_days
    return render(request, 'home.html', context)

#登录模态框
def login_for_modal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)
