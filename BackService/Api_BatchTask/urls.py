from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'SelectData', views.select_data, name='SelectData'),
    url(r'CreateHookId', views.create_hook_id, name='CreateHookId'),
    url(r'SelectTaskData', views.select_task_data, name='SelectTaskData'),
    url(r'CharmBatchData', views.charm_batch_data, name='CharmBatchData'),
    url(r'SaveData', views.save_data, name='SaveData'),
    url(r'LoadBatchData', views.load_batch_data, name='LoadBatchData'),
    url(r'EditData', views.edit_data, name='EditData'),
    url(r'DeleteData', views.delete_data, name='DeleteData'),
    url(r'ExecuteBatchTask', views.execute_batch_task, name='ExecuteBatchTask'),
    url(r'ExecutiveLogging', views.executive_logging, name='ExecutiveLogging'),
    url(r'RunHookTask', views.run_hook_task, name='RunHookTask'),
    url(r'SelectHistory', views.select_history, name='SelectHistory'),
    url(r'RestorData', views.restor_data, name='RestorData'),


]
