from django.conf.urls import url, include
from . import views

app_name = 'home'

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^accounts/register/$', views.Register.as_view(), name="register"),
    url(r'^account/activate/$', views.activate_account, name="activate_user"),
]