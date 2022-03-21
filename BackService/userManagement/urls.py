from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'SelectData', views.select_data, name='SelectData'),
    url(r'UserActivation', views.user_activation, name='UserActivation'),
    url(r'EditIsLockState', views.edit_islock_state, name='EditIsLockState'),
    url(r'DeleteData', views.delete_data, name='DeleteData'),
    url(r'EditData', views.edit_data, name='EditData'),
    url(r'InternalRegistered', views.internal_registered, name='InternalRegistered'),
    url(r'GetUserNameItems', views.get_user_name_items, name='GetUserNameItems'),
]
