from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'SelectData', views.select_data, name='SelectData'),
    url(r'SelectCaseData', views.select_case_data, name='SelectCaseData'),
    url(r'CharmTaskData', views.charm_task_data, name='CharmTaskData'),
    url(r'SaveData', views.save_data, name='SaveData'),
    url(r'LoadTaskData', views.load_task_data, name='LoadTaskData'),
    url(r'EditData', views.edit_data, name='EditData'),
    url(r'DeleteData', views.delete_data, name='DeleteData'),
    url(r'SelectHistory', views.select_history, name='SelectHistory'),
    url(r'RestorData', views.restor_data, name='RestorData'),
    url(r'ExecuteTask', views.execute_task, name='ExecuteTask'),
    url(r'ExecutiveLogging', views.executive_logging, name='ExecutiveLogging'),
]
