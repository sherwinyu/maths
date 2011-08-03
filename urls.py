from django.conf.urls.defaults import patterns, include, url
from maths.views import *
from django.views.generic.simple import *
from forms import AnswerForm

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^hello/$', hello_world),
	url(r'^search-form/$', search),
	url(r'^search/$', search),
	url(r'^contact/$', contact),
	url(r'^xhr_test/$', xhr_test),
	url(r'^ajax_test/$', direct_to_template, {'template': 'ajax_test.html'}),
	url(r'^play/submitAnswer/ajax/?$', submitAnswer),
	url(r'^play/submitAnswer/?$', submitAnswer),
	url(r'^play/$', direct_to_template, {'template': 'play.html', 'extra_context': {'form': AnswerForm() } }),

    # Examples:
    # url(r'^$', 'maths.views.home', name='home'),
    # url(r'^maths2/', include('maths2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
