from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'LoadUserInfo', views.load_user_info, name='LoadUserInfo'),
    url(r'SaveUserInfo', views.save_user_info, name='SaveUserInfo'),
    url(r'GetHomePermissions', views.get_home_permissions, name='GetHomePermissions'),
    url(r'GetPermissions', views.get_permissions, name='GetPermissions'),
    url(r'GetRouterPath', views.get_router_path, name='GetRouterPath'),
    url(r'GetUserStatisticsInfo', views.get_user_statistics_info, name='GetUserStatisticsInfo'),
    url(r'GetServerIndicators', views.get_server_indicators, name='GetServerIndicators'),
    url(r'ApiPageHomeSelectTestResults', views.api_pagehome_select_test_results, name='ApiPageHomeSelectTestResults'),
    url(r'ApiPageHomeSelectPageStatistical', views.api_pagehome_select_page_statistical, name='ApiPageHomeSelectPageStatistical'),
    url(r'ApiPageHomeSelectProStatistical', views.api_pagehome_select_pro_statistical, name='ApiPageHomeSelectProStatistical'),
    url(r'ApiPageHomeSelectFormerlyData', views.api_pagehome_select_Formerly_data, name='ApiPageHomeSelectFormerlyData'),
    url(r'ApiPageHomeSelectProQueue', views.api_pagehome_select_pro_queue, name='ApiPageHomeSelectProQueue'),
    url(r'ApiPageHomeHandleState', views.api_pagehome_handle_state, name='ApiPageHomeHandleState'),
    url(r'ApiPageMainDataRefresh', views.api_page_get_main_data, name='ApiPageMainDataRefresh'),
    url(r'SelectSysTotal', views.select_sys_total, name='SelectSysTotal'),
    url(r'SelectUserTotal', views.select_user_total, name='SelectUserTotal'),
]