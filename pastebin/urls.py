from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<paste_hash>[0-9]+)/$', views.detail, name='detail'),
    url(r'^new/', views.new_paste, name='new'),
]

