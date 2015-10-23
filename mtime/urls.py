from django.conf.urls import url,patterns

from . import views

urlpatterns = patterns('mtime',
    # url(r'^$', views.index, name='index'),
    url(r'^index2/$', views.index2, name='index2'),
    # url(r'(?P<question_id>[0-9]+)/$',views.detail,name='detail'),
    # # ex: /polls/5/results/
    # url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # # ex: /polls/5/vote/
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    
    #generic views
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),

    #tem view
    # 1
    #url(r'^about/', views.TemplateView.as_view(template_name="about.html")),
    # 2
    url(r'^about/', views.AboutView.as_view()),
#blog
    url(r'^post/$', views.post_list,name='blog'), 
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail,name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),

#form test
    url(r'^contact_author/$', views.contact_author,name="contact_author"),
    url(r'^thanks/$', views.thanks,name='thanks'),    
    url(r'^hostlist/$', views.HostsList,name="HostsList"),  
    url(r'^create_host/$',views.create_host),  
)
