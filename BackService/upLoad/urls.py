from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'UpLoadToTempPath', views.upLoad_to_temp_path, name='UpLoadToTempPath'),  # 上传到临时目录中
]
