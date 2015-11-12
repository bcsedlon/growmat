from django.conf.urls import url, include


from . import views

from .models import InstrumentList
from .views import InstrumentCreate, InstrumentUpdate, InstrumentDelete, RuleDelete, PeriodDelete

urlpatterns = [
	#url(r'^$', views.index, name='index'),
	url(r'^archive/(?P<pk>[0-9]+)/$', views.archive, name='archive'),
	url(r'^archive/$', views.archive, name='archive'),
	

	url(r'^save/$', views.save, name='save'),
	
	url(r'^rule/$', views.rule, name='rule'),
	url(r'^rule/(?P<pk>[0-9]+)/$', views.rule, name='rule'),
	url(r'^rule_delete/(?P<pk>[0-9]+)/$', RuleDelete.as_view(), name='rule_delete'),
	
	url(r'^period/$', views.period, name='period'),
	url(r'^period/(?P<pk>[0-9]+)/$', views.period, name='period'),
	url(r'^period_delete/(?P<pk>[0-9]+)/$', PeriodDelete.as_view(), name='period_delete'),
	
	url(r'^(?P<pk>[0-9]+)/$', views.index, name='index'),
	url(r'^$', views.index, name='index'),
	
	url(r'^webcam/$', views.webcam, name='webcam'),
	
	url(r'^(?P<instrument_id>[0-9]+)/$', views.instrument, name='instrument'),
	url(r'^instrumentAdd/$', views.instrumentAdd, name='instrumentAdd'),
	url(r'^list/$', InstrumentList.as_view()),
	url(r'^c/$', InstrumentCreate.as_view(), name='c'),
	#url(r'^u/(?P<pk>[0-9]+)$', InstrumentUpdate.as_view(), name='u'),
	#url(r'^u/(?P<pk>[0-9]+)$', views.update(), name='u'),
	url(r'^d/(?P<pk>[0-9]+)$', InstrumentDelete.as_view(), name='d'),
	#url(r'^d/(?P<pk>[0-9]+)$', InstrumentDelete.as_view()), name='d'),	
	url(r'^list$', InstrumentList.as_view(), name='list'),
	
	#url(r'^', include('django.contrib.auth.urls')),
	url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
	url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'registration/logged_out2.html'}, name='logout'),

	
]