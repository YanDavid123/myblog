from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    #http://localhost:8000/blog/
    path('',views.blog_list,name='blog_list'),
    path('<int:blog_pk>',views.blog_detail,name="blog_detail"),
    path('type/<int:blog_type_pk>',views.blog_with_type,name="blogs_with_type"),
    path('date/<int:year>/<int:month>',views.blog_with_date,name="blogs_with_date"),
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)