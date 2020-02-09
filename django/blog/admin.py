from django.contrib import admin
from .models import Post

# Register your models here.


#포스트 카테고리를 추가
admin.site.register(Post)