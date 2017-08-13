from django.conf.urls import url
from django.contrib.auth.views import login, logout

from . import views

urlpatterns = [
    #url(r'^accounts/login/$', login, name = 'login'),
    url(r'^$', views.index, name='index'),
    #url(r'login', views.login, name='login')
    # Login/Logout URLs
    #url(r'^login/$',views.login),
    url(r'^login/$',login, {'template_name': 'pharmeasyflow/login.html'}, name = 'login'),
    url(r'^logout/$',logout, {'next_page': '/pharm/login/'}),
    url(r'^signup/$', views.signup),
    url(r'^profile/$', views.profile),
    url(r'^doctor_profile', views.doctor_profile, name='doctor_profile'),
    url(r'^patient_profile', views.patient_profile, name='patient_profile'),
    url(r'^pharmacist_profile', views.pharmacist_profile, name='pharmacist_profile')
    
]