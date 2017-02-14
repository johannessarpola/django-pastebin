from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<paste_hash>\d+)/$', views.detail, name='detail'),
    url(r'^invalid', views.invalid_hash, name='invalid_hash'),
    url(r'^new', views.new_paste, name='new'),
    url(r'^login', views.login_view, name='login'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^register', views.register_user, name='register'),
    url(r'^forgot', views.forgot_password, name='forgot'),
    url(r'^me', views.profile, name='profile'),
    url(r'^about', views.about, name='about'),
    url(r'^view/(?P<paste_hash>\d+)', views.view_paste, name='view'),
]

