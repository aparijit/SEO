from django.conf.urls import url
#from django.conf.urls.defaults import *
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^list/', views.list, name='urllist'),
]
