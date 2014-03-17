from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wechat.views.home', name='home'),
    url(r'^demo/', include('demo.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
