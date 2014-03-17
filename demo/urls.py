# -*- encoding:utf-8 -*-
__author__ = 'Cheny'

from django.conf.urls import patterns, url
from .views import wx_sign

urlpatterns = patterns('',
                       url(r'^sign/$', wx_sign, name='home'),

)
