# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from spyne.application import Application
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from django.views.decorators.csrf import csrf_exempt
from soapwebservice.models import SDPSimulator, SMSGATEWAY_TARGET_NAMESPACE


__author__ = "Zeinab Abbasimazar -> https://github.com/zeinababbasi"


app = Application(services=[SDPSimulator],
                  tns=SMSGATEWAY_TARGET_NAMESPACE,
                  name='SendSmsWebService',
                  in_protocol=Soap11(validator='lxml'),
                  out_protocol=Soap11(),
                  )


soapwebservice = csrf_exempt(DjangoApplication(app))
