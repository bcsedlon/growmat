from django.conf.urls import url

from . import views

from .models import InstrumentList
from .views import InstrumentCreate, InstrumentUpdate, InstrumentDelete, RuleDelete

urlpatterns = [
	#url(r'^$', views.index, name='index'),
	url(r'^archive/(?P<pk>[0-9]+)/$', views.archive, name='archive'),
	url(r'^archive/$', views.archive, name='archive'),
	
	url(r'^rule/$', views.rule, name='rule'),
	url(r'^rule/(?P<pk>[0-9]+)/$', views.rule, name='rule'),
	url(r'^rule_delete/(?P<pk>[0-9]+)/$', RuleDelete.as_view(), name='rule_delete'),
	
	url(r'^(?P<pk>[0-9]+)/$', views.index, name='index'),
	url(r'^$', views.index, name='index'),
	
	
	
	url(r'^(?P<instrument_id>[0-9]+)/$', views.instrument, name='instrument'),
	url(r'^instrumentAdd/$', views.instrumentAdd, name='instrumentAdd'),
	url(r'^list/$', InstrumentList.as_view()),
	url(r'^c/$', InstrumentCreate.as_view(), name='c'),
	#url(r'^u/(?P<pk>[0-9]+)$', InstrumentUpdate.as_view(), name='u'),
	#url(r'^u/(?P<pk>[0-9]+)$', views.update(), name='u'),
	url(r'^d/(?P<pk>[0-9]+)$', InstrumentDelete.as_view(), name='d'),
	#url(r'^d/(?P<pk>[0-9]+)$', InstrumentDelete.as_view()), name='d'),	
	url(r'^list$', InstrumentList.as_view(), name='list'),
	

	
]