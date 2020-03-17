import threading
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

class SendEmail(threading.Thread):
    def __init__(self,subjct,text,email,fail_silently=False):
        self.subjct = subjct
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def send(self):
        send_mail(self.subjct,self.text,settings.EMAIL_HOST_USER,[self.email],fail_silently=self.fail_silently)

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='用户')

    root = models.ForeignKey('self',null=True,related_name='root_comment',on_delete=models.CASCADE)
    parent = models.ForeignKey('self',null=True,related_name='parent_comment',on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User,null=True,related_name='replies',on_delete=models.CASCADE)

    def send_email(self):
        if not self.parent is None:
            #评论我的邮箱
            subjct = '有人评论你的博客'
            email = self.content_object.get_email()
        else:
            #回复评论
            subjct = '有人回复你的评论'
            email = self.reply_to.email()
        if email != '':
            text = self.text + '\n' + self.content_object.get_url()
            send_email = SendEmail(subjct,text,email)
            send_email.start()

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']