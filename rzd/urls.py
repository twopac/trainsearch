# -*- coding: utf-8 -*-
import settings

from django.views.generic import TemplateView
from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import suggester, trains

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^suggester/$', suggester, name='suggester'),
    url(r'^search/trains/$', trains, name='trains'),

)
