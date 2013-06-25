from django.conf.urls import patterns, url

from manager import views

urlpatterns = patterns('',
    url(r'^$', views.index2, name='index2'),
    url(r'^view/$', views.view, name='view'),
    url(r'^add/$', views.add, name='add'),
    url(r'^contact_us/$', views.contact_us, name='contact_us'),
    url(r'^handle_add/$', views.handle_add, name='handle_add'),
    url(r'^view/edit/(?P<id>\d+)/$', views.edit, name='edit'),
    url(r'^view/delete/(?P<id>\d+)/$', views.delete, name='delete'),
    url(r'api/post_data', views.post_config),
    url(r'^exp/$', views.exp, name='exp'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^adminpage/$', views.adminpage, name='adminpage'),
    url(r'^handle_edit/$', views.handle_edit, name='handle_edit'),
    url(r'^add_offline_stock/$', views.add_offline_stock, name='add_offline_stock'),
    url(r'^view_offline_stock/$', views.view_offline_stock, name='view_offline_stock'),
    url(r'^handle_offline_add/$', views.handle_offline_add, name='handle_offline_add'),
    url(r'^view_offline_stock/edit/(?P<id>\d+)$', views.editoffline, name='editoffline'),
    url(r'^view_offline_stock/delete/(?P<id>\d+)$', views.deleteoffline, name='deleteoffline'),
    url(r'^handle_offline_edit/$', views.handle_offline_edit, name='handle_offline_edit'),
    url(r'^expoffline/$', views.expoffline, name='expoffline'),
    url(r'^expfull/$', views.expfull, name='expfull'),
    url(r'^search/$', views.search, name='search'),
    url(r'^searchoffline/$', views.searchoffline, name='searchoffline'),
)   
