from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'SelectData', views.select_data, name='SelectData'),
    url(r'SaveData', views.save_data, name='SaveData'),
    url(r'EditData', views.edit_data, name='EditData'),
    url(r'DeleteData', views.delete_data, name='DeleteData'),
    url(r'CharmEventData', views.charm_event_data, name='CharmEventData'),
    url(r'LoadData', views.load_data, name='LoadData'),
    url(r'LoadOperationData', views.load_operation_data, name='LoadOperationData'),
    url(r'UpdateOperationSort', views.update_operation_sort, name='UpdateOperationSort'),
    url(r'GetElementOperationTypeItems', views.get_element_operation_type_items, name='GetElementOperationTypeItems'),
]
