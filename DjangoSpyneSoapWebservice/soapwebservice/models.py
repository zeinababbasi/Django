# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from spyne.decorator import rpc
from spyne.service import ServiceBase
from spyne.model.complex import ComplexModel
from spyne.model.primitive import Unicode, Int, String, Long, Integer
from spyne.model.fault import Fault
import re
import time


__author__ = "Zeinab Abbasimazar -> https://github.com/zeinababbasi"


# Messages
SOAP_FAULT_CODE = 'soap:Server'
SOAP_FAULT_DETAIL = '<ns1:SOAPWEbServerException xmlns:ns1=\"https://github.com/zeinababbasi/\"/>'
SOAP_FAULT_INTERNAL_ERROR_STRING = 'Internal error'
SOAP_INVALID_NUMBER_VALUE_MESSAGE = 'Unmarshalling Error: Not a number:'
SOAP_INVALID_STRING_VALUE_MESSAGE = 'Unmarshalling Error: Not a normal string:'
SOAP_MANDATORY_FIELD_NOT_PRESENT_MESSAGE = 'Mandatory field is not present:'

# Django-Spyne SOAP Web Server WSDL Properties
SOAP_WEB_SERVER_SERVICE_NAME = 'SOAPWebService'
SOAP_WEB_SERVER_TARGET_NAMESPACE = 'https://github.com/zeinababbasi/'
SOAP_WEB_SERVER_EXCEPTION_TAG_NAME = 'ns1:SOAPWEbServerException'

# Status / Status Codes
STATUS_CODE = 6
STATUS = 'Success'


class Status(ComplexModel):
    __namespace__ = SOAP_WEB_SERVER_TARGET_NAMESPACE
    status = Int
    status_date = Int
    msg_id = Long
    msg_title = Unicode
    msg_source = Integer


class ReturnValueGetStatus(ComplexModel):
    __namespace__ = SOAP_WEB_SERVER_TARGET_NAMESPACE
    error_msg = String
    status = Int
    report_item = Status


class RespCode(ComplexModel):
    __namespace__ = SOAP_WEB_SERVER_TARGET_NAMESPACE
    resp_status = Int


class SOAPWebServerException(Fault):
    __namespace__ = SOAP_WEB_SERVER_TARGET_NAMESPACE

    def __init__(self, message):
        super(SOAPWebServerException, self).__init__(
            faultcode=SOAP_FAULT_CODE, faultstring=message,
            detail={SOAP_WEB_SERVER_EXCEPTION_TAG_NAME: SOAP_WEB_SERVER_TARGET_NAMESPACE})


class SOAPWebServer(ServiceBase):

    __service_name__ = SOAP_WEB_SERVER_SERVICE_NAME

    @rpc(Int, Unicode, Integer, _returns=ReturnValueGetStatus.customize(sub_name='return'))
    def get_status(ctx, msg_id, msg_title, msg_source):
        # Check if mandatory fields are present
        if msg_id is None:
            return ReturnValueGetStatus(error_msg='%s \"msg_id\"' % SOAP_MANDATORY_FIELD_NOT_PRESENT_MESSAGE, status=1)

        # Check if fields' values are valid
        if re.match(r'^\d+$', str(msg_id)) is None:
            return SOAPWebServerException(message='%s \"%s\"' % (SOAP_INVALID_STRING_VALUE_MESSAGE, str(msg_id)))

        deliver_date = str(int(time.time()))
        report_item = Status(status_date=deliver_date, status=STATUS_CODE,
                             msg_id=msg_id, msg_title=msg_title, msg_source=msg_source)
        result = ReturnValueGetStatus(status=0, repor_item=report_item)
        return result

    @rpc(Int, _returns=RespCode)
    def set_status_code(ctx, status_code):
        global STATUS_CODE
        STATUS_CODE = int(status_code)
        return RespCode(resp_status=0)

    @rpc(Int, _returns=RespCode)
    def set_status(ctx, status):
        global STATUS
        STATUS = status
        return RespCode(resp_status=0)
