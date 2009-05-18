from django.conf.urls.defaults import *


urlpatterns = patterns('django.views.generic.simple',
    (r'^test/$', 'direct_to_template', {'template': 'original.html'}),
    (r'^other/$', 'direct_to_template', {'template': 'other.html'}),
    (r'^goal/$', 'direct_to_template', {'template': 'goal.html'}),
)