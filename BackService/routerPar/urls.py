from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'SelectData', views.select_data, name='SelectData'),
    url(r'GetPreviewData', views.get_preview_data, name='GetPreviewData'),
    url(r'GetBelogIdTable', views.get_belogid_table, name='GetBelogIdTable'),
    url(r'SaveData', views.save_data, name='SaveData'),
    url(r'EditData', views.edit_data, name='EditData'),
    url(r'DeleteData', views.delete_data, name='DeleteData'),
    url(r'UpdateRouterSort', views.update_router_sort, name='UpdateRouterSort'),
    url(r'LoadRouterData', views.load_router_data, name='LoadRouterData'),
]
