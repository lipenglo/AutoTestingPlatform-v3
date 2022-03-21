from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'TestConnect', views.test_connect, name='TestConnect'),
    url(r'SaveData', views.save_data, name='SaveData'),
    url(r'EditData', views.edit_data, name='EditData'),
    url(r'DeleteData', views.delete_data, name='DeleteData'),
    url(r'GetConnectBaseItems', views.get_connect_base_items, name='GetConnectBaseItems'),
    # url(r'SelectHistory', views.select_history, name='SelectHistory'),
    url(r'SelectData', views.select_data, name='SelectData'),
]
