from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    
    #정규표현식을 이용하여 파싱하기
    #d+ : 숫자가 얼마가 오든 처리하겠다.
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name = 'post_detail'),
    url(r'^post/new/', views.post_new, name ='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name = 'post_edit'),
]