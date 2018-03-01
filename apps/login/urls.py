from django.conf.urls import url
from . import views  
        
urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.main),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^travels$', views.travels),
    url(r'^travels/add$', views.add_destination),
    url(r'^process_destination$', views.process_destination),
    url(r'^add_destination/(?P<id>\d+)$', views.join_destination),
    url(r'^travels/destination/(?P<id>\d+)$', views.view_destination),  
]