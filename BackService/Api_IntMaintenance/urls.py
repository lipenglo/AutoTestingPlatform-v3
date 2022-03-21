from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'SelectData', views.select_data, name='SelectData'),
    url(r'SaveData', views.save_data, name='SaveData'),
    url(r'EditData', views.edit_data, name='EditData'),
    url(r'DeleteData', views.delete_data, name='DeleteData'),
    url(r'CharmApiData', views.charm_api_data, name='CharmApiData'),
    url(r'LoadData', views.load_data, name='LoadData'),
    url(r'SendRequest', views.send_request, name='SendRequest'),
    url(r'SendTestRequest', views.send_test_request, name='SendTestRequest'),
    url(r'CopyApi', views.copy_api, name='CopyApi'),
    url(r'SelectHistory', views.select_history, name='SelectHistory'),
    url(r'RestorData', views.restor_data, name='RestorData'),
    url(r'SelectLifeCycle', views.select_life_cycle, name='SelectLifeCycle'),
    url(r'AnalysisJsonData', views.analysis_json_data, name='AnalysisJsonData'),
    url(r'ImportApiData', views.import_api_data, name='ImportApiData'),

]
