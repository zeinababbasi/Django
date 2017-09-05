# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from django.core.wsgi import get_wsgi_application
import os


__author__ = "Zeinab Abbasimazar -> https://github.com/zeinababbasi"


"""
WSGI config for DjangoSpyneSoapWebservice project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
application = get_wsgi_application()
