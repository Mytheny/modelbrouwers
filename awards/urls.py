from django.conf.urls.defaults import *

urlpatterns = patterns('awards.views',
    (r'^nomination/$', 'nomination'),
#    (r'^nomination/(\d+)/$', 'nomination_detail'),
    (r'^vote/$', 'vote'),
    (r'^vote/overview/$', 'vote_overview'),
    (r'^vote/scores/$', 'scores'),
    (r'^categories/$', 'category'),
    (r'^categories/(\d+)/$', 'category_list_nominations'),
    (r'^winners/$', 'winners'),
    )

urlpatterns += patterns('django.views.generic.simple',
    url(r'^$', 'direct_to_template', {'template': 'awards/base.html'}, name='awards_index'),
    )
