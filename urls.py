from django.conf.urls.defaults import patterns, include, url
from maths.views import *
from django.views.generic.simple import *
from forms import AnswerForm

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^play/submitAnswer/ajax$', submitAnswer),
	url(r'^play/$', newSession),

    # Examples:
    # url(r'^$', 'maths.views.home', name='home'),
    # url(r'^maths2/', include('maths2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
