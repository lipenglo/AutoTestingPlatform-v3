from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'SelectData', views.select_data, name='SelectData'),
    url(r'SaveData', views.save_data, name='SaveData'),
    url(r'EditData', views.edit_data, name='EditData'),
    url(r'DeleteData', views.delete_data, name='DeleteData'),
    url(r'LoadData', views.load_data, name='LoadData'),
    url(r'CharmElementData', views.charm_element_data, name='CharmElementData'),
    url(r'SelectHistory', views.select_history, name='SelectHistory'),
    url(r'JoinMembers', views.copy_element, name='JoinMembers'),
    url(r'CopyElement', views.copy_element, name='CopyElement'),
    url(r'GetElementNameItems', views.get_element_name_items, name='GetElementNameItems'),
    url(r'SelectElementType', views.select_element_type, name='SelectElementType'),
    url(r'RestorData', views.restor_data, name='RestorData'),
    url(r'SelectLifeCycle', views.select_life_cycle, name='SelectLifeCycle'),
]
