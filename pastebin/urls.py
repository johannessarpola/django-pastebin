from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<paste_hash>\d+)/$', views.detail, name='detail'),
    url(r'^invalid/', views.invalid_hash, name='invalid_hash'),
    url(r'^new/', views.new_paste, name='new'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^register/', views.register_user, name='register'),
]

