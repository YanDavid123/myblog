import datetime
from django.db.models import Sum
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum
from .models import ReadDetail


#阅读量数量
def read_statistics_once_read(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    print('ctshism',ct)
    key = ("%s_%s_read" % (ct.model,obj.pk))

    if not request.COOKIES.get(key):
        readnum,created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        #日期统计
        date = timezone.now().date()
        readDetail,created = ReadDetail.objects.get_or_create(content_type=ct,object_id=obj.pk,date=date)
        readDetail.read_num +=1
        readDetail.save()
    return key

#看前七天每天的阅读量
def get_seven_days_read_data(conten_type):
    today = timezone.now().date()
    print("today是:",today)
    dates = []
    read_nums = []
    for i in range(6,-1,-1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=conten_type,date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates,read_nums









