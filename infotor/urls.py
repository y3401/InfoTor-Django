from django.conf.urls import url

from . import views

app_name = 'infotor'
urlpatterns = [
#    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<file_id>[0-9]+)/$', views.info, name='info'),
    url(r'^search/', views.search, name='search'),
#    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
#    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]