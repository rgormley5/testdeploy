from django.conf.urls import url
from . import views  
        
urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.main),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^wish_items/create$', views.add_item),
    url(r'^process_item$', views.process_item),
    url(r'^remove$', views.remove),
    url(r'^delete$', views.delete),
    url(r'^wish_items/(?P<id>\d+)$', views.view_item),
    url(r'^add_list/(?P<id>\d+)$', views.add_list),
    # url(r'^remove_list/(?P<id>\d+)$', views.remove_list),
    
]