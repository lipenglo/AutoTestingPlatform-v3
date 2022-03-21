from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'SelectData', views.select_data, name='SelectData'),
    url(r'SaveData', views.save_data, name='SaveData'),
    url(r'EditData', views.edit_data, name='EditData'),
    url(r'DeleteData', views.delete_data, name='DeleteData'),
    url(r'NoTokenGetRoleNameItems', views.no_token_get_role_name_items, name='NoTokenGetRoleNameItems'),
    url(r'GetRoleNameItems', views.get_role_name_items, name='GetRoleNameItems'),
    url(r'GetMenuList', views.get_menu_list, name='GetMenuList'),
    url(r'SaveRolePermissions', views.save_role_permissions, name='SaveRolePermissions'),
]
