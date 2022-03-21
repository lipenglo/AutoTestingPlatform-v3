from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'SelectData', views.select_data, name='SelectData'),
    # url(r'SaveData', views.save_data, name='SaveData'),
    # url(r'EditData', views.edit_data, name='EditData'),
    url(r'DeleteData', views.delete_data, name='DeleteData'),
    url(r'loadReportData', views.load_report_data, name='loadReportData'),
    url(r'LoadReportApi', views.load_report_api, name='LoadReportApi'),
    # url(r'loadReportCase', views.load_report_case, name='loadReportCase'),
    url(r'SelectLastReport', views.select_last_report, name='SelectLastReport'),
]
