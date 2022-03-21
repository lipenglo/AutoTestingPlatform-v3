from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'SelectData', views.select_data, name='SelectData'),
    url(r'SaveData', views.save_data, name='SaveData'),
    url(r'EditData', views.edit_data, name='EditData'),
    url(r'DeleteData', views.delete_data, name='DeleteData'),
    url(r'GetPageNameItems', views.get_page_name_items, name='GetPageNameItems'),
    url(r'SelectHistory', views.select_history, name='SelectHistory'),
    url(r'RestorData', views.restor_data, name='RestorData'),
    url(r'GetAssociatedPageNameItems', views.get_associated_page_name_items, name='GetAssociatedPageNameItems'),
]
