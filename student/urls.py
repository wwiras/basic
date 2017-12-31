from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required
# import views

urlpatterns = [
    url(r'^list/$', views.student_list, name='student_list'),
    url(r'^new/$', views.student_new, name='student_new'),
    url(r'^(?P<pk>\d+)/edit$', views.student_edit, name='student_edit'),
    url(r'^(?P<pk>\d+)/remove$', views.student_remove, name='student_remove'),
    url(r'^(?P<pk>\d+)/$', views.student_detail, name='student_detail'),
    url(r'^home/$', views.home, name='student_home2'),
    url(r'^$', views.home_json, name='student_home'),
    url(r'^list_json/$', login_required(views.student_list_json.as_view()), name="student_list_json"),
    # url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    # url(r'^post/new/$', views.post_new, name='post_new'),
    # url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    # url(r'student_list/$', views.StudentListJson.as_view(), name="student_list_json"),
    # url(r'^student_list/$', views.StudentListJson, name="student_list_json"),
]