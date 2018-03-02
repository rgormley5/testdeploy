from django.conf.urls import url
from . import views  
        
urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.main),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^quotes$', views.quotes),
    url(r'^process_quote$', views.process_quote),
    url(r'^add_quote/(?P<id>\d+)$', views.add_quote),
    url(r'^remove_quote/(?P<id>\d+)$', views.remove_quote),
    url(r'^users/(?P<id>\d+)$', views.show_user),
    
    # url(r'^travels/destination/(?P<id>\d+)$', views.view_destination),  
    # url(r'^travels/add$', views.add_destination),
]