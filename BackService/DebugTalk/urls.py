from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'SelectData', views.select_data, name='SelectData'),
    url(r'DataSave', views.data_save, name='DataSave'),
    url(r'RunDebug', views.run_debug, name='RunDebug'),
]
