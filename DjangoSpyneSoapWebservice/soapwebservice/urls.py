# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from django.conf.urls import url
from soapwebservice import views


__author__ = "Zeinab Abbasimazar -> https://github.com/zeinababbasi"


urlpatterns = [
    url(r'^services/SendSms', views.soapwebservice),
]
