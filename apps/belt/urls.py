from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='my_index'),
    url(r'^register$', views.register, name='my_reg'),
    url(r'^travels$', views.travels, name='my_show'),
    url(r'^login$', views.login, name='my_login'),
    url(r'^logout$', views.logout, name='my_logout'),
    url(r'^travels/add$', views.add_plan, name='my_plan'),
    url(r'^add_trip$', views.add_trip, name='my_trip'),
    url(r'^destination/(?P<trip_id>\d+)$', views.destination, name='my_destination'),
    url(r'^join/(?P<trip_id>\d+)$', views.join_trip, name='join_trips')
]
