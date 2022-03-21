from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'SelectOperationalInfo', views.select_operational_info, name='SelectOperationalInfo'),
    url(r'UserOperationalInfo', views.user_operational_info, name='UserOperationalInfo'),
    url(r'EditIsReadState', views.edit_isread_state, name='EditIsReadState'),
    url(r'EditOperationalInfoState', views.edit_operational_info_state, name='EditOperationalInfoState'),
    url(r'SettingOperationalReadAll', views.setting_operational_read_all, name='SettingOperationalReadAll'),
]
