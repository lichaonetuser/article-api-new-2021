# coding=utf-8
from __future__ import absolute_import
from django.conf.urls import url
import api.video.views as views


urlpatterns = [
    url(r'^url/$', views.url),
    url(r'^url_report/$', views.url_report),
]
