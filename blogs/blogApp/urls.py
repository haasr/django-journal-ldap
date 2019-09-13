from django.conf.urls import url
from blogApp import views

app_name = 'blogApp'

urlpatterns=[
    url(r'^register/$', views.register,name='register'),
    url(r'^user_login/$', views.user_login,name='user_login')
]
