from django.urls import re_path
from blogApp import views

app_name = 'blogApp'

urlpatterns=[
    re_path(r'^register/$', views.register,name='register'),
    re_path(r'^user_login/$', views.user_login,name='user_login'),
    re_path(r'^blog/', views.blogView, name='blogViewUrl')
]
