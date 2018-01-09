from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from iGo import env
from . import views

content = {}
content['server'] = env.content

urlpatterns = [
    url(r'^', include('home.urls')),
    url(r'^accounts/login/$', auth_views.login, {'extra_context': content}, name="login"),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^admin/', admin.site.urls)
]

handler404 = views.handler404
handler500 = views.handler500