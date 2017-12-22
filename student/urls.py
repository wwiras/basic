from django.conf.urls import url
from . import views
# import views

urlpatterns = [
    url(r'^list/$', views.student_list, name='student_list'),
    url(r'^new/$', views.student_new, name='student_new'),
    url(r'^(?P<pk>\d+)/edit$', views.student_edit, name='student_edit'),
    url(r'^(?P<pk>\d+)/remove$', views.student_remove, name='student_remove'),
    url(r'^(?P<pk>\d+)/$', views.student_detail, name='student_detail'),
    url(r'^$', views.home, name='student_home'),
    # url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    # url(r'^post/new/$', views.post_new, name='post_new'),
    # url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
]