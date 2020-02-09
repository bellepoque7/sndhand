from django.conf import settings
from django.db import models
from django.utils import timezone



# Create your models here.
class Post(models.Model):
    
    #다른모델에 대한 링크
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #문자열이 제한있는 필드
    title = models.CharField(max_length=200)
    #문자열 제한이 없는 필드
    text = models.TextField()
    #날짜와 시간
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    #동작 정의
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    #하기 함수를 호충하면 제목을 반환해줄 것
    def __str__(self):
        return self.title