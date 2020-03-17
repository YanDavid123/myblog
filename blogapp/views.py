from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from .models import Blog,BlogType
from django.db.models import Count
from read_statistics.utils import read_statistics_once_read
import datetime
from django.utils import timezone
from .models import ReadDetail
from django.contrib.contenttypes.models import ContentType


# Create your views here.
def get_blog_list_common_data(request,blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)  # 每6篇进行分页
    page_num = request.GET.get('page', 1)  # 获取url的页面参数（GET请求）
    page_of_blogs = paginator.page(page_num)
    curenter_page_num = page_of_blogs.number  # 获取当前页码
    page_range = list(
        filter(lambda x: 0 < x <= paginator.num_pages, range(curenter_page_num - 3, curenter_page_num + 2)))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    #获取博客分类的对应博客数量
    '''blog_types = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_types_list.append(blog_type)
     '''
    #获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time','month',order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

#热门博客查找
    blog_content_type = ContentType.objects.get_for_model(Blog)
    # 今日阅读量排行榜
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=blog_content_type, date=today).order_by('-read_num')
    # 昨天热门博客排行榜
    yesterday = today - datetime.timedelta(days=1)
    read_details_yes = ReadDetail.objects.filter(content_type=blog_content_type, date=yesterday).order_by('-read_num')


    context = {}
    #当页面显示的所有博客
    context['blogs'] = page_of_blogs.object_list

    #页码数
    context['page_range'] = page_range

    #所有博客的对象
    context['page_of_blogs'] = page_of_blogs

    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))   #获取所有博客分类,blog_count=对应博客数量
    context['blog_dates'] = blog_dates_dict        #获取日期归档对应的博客数量
    context['today_hot_data'] = read_details
    context['yesterday_hot_data'] = read_details_yes
    return context

def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request,blogs_all_list)
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request,blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    #阅读计数对象的调用
    read_cookie_key = read_statistics_once_read(request,blog)

    context = {}
    context['blog'] = blog

    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    response = render(request, 'blog/blog_detail.html', context)    #响应
    #Cookie阅读计数保存下来
    response.set_cookie(read_cookie_key,'true')   #这样关掉页面才重置，重新打开页面计数，后面加max_age= 自定义以秒为单位的再次计数时间
    return response

def blog_with_type(request,blog_type_pk):
    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request,blogs_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog/blog_with_type.html',context)

def blog_with_date(request,year,month):
    blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
    context = get_blog_list_common_data(request,blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' %(year,month)
    return render(request, 'blog/blog_with_date.html', context)


