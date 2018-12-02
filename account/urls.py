from django.conf.urls import url, include

from django.contrib.auth import views as auth_views

from account.views import signup

urlpatterns = [

    url('^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url('^signup/$', signup, name='signup'),
    url('logout/$', auth_views.LogoutView.as_view(), name='logout')

]
