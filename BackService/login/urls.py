from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'registered', views.registered, name='registered'),  # 注册用户
    url(r'loginIn', views.login_in, name='loginIn'),
]
