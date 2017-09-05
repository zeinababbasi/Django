# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from spyne.decorator import rpc
from spyne.service import ServiceBase
from spyne.model.complex import ComplexModel
from spyne.model.primitive import Unicode, Int, String, Long
from spyne.model.fault import Fault
import re
import time
import random
import string


__author__ = "Zeinab Abbasimazar -> https://github.com/zeinababbasi"


# SOAP Messages
SOAP_FAULT_CODE = 'soap:Server'
SOAP_FAULT_DETAIL = '<ns1:SMSGatewayException xmlns:ns1=\"http://webservice.smsgateway.services.sdp.peykasa.com/\"/>'
SOAP_FAULT_INTERNAL_ERROR_STRING = 'Internal error'
SOAP_INVALID_NUMBER_VALUE_MESSAGE = 'Unmarshalling Error: Not a number:'
SOAP_INVALID_STRING_VALUE_MESSAGE = 'Unmarshalling Error: For input string:'

# SMS Gateway WSDL Properties
SMSGATEWAY_SERVICE_NAME = 'SendSmsWebServiceImplService'
SMSGATEWAY_TARGET_NAMESPACE = 'http://webservice.smsgateway.services.sdp.peykasa.com/'
SMSGATEWAY_EXCEPTION_TAG_NAME = 'ns1:SMSGatewayException'

# SMS Gateway Messages
SMSGATEWAY_MANDATORY_SOURCE_ADDRESS_MESSAGE = 'Source address is mandatory'
SMSGATEWAY_MANDATORY_DESTINATION_ADDRESS_MESSAGE = 'Destination address is mandatory'
SMSGATEWAY_MANDATORY_MESSAGE_BODY_MESSAGE = 'Message body is mandatory'
SMSGATEWAY_MANDATORY_MESSAGE_ENCODING_MESSAGE = 'Message encoding is mandatory'
SMSGATEWAY_MANDATORY_GROUP_ID_MESSAGE = 'GroupId is mandatory'
SMSGATEWAY_EMPTY_MESSAGE_ID_ARRAY_MESSAGE = 'msgIdArray is empty'
SMSGATEWAY_INVALID_MESSAGE_ENCODING_MESSAGE = 'At least one of message encodings is invalid'
SMSGATEWAY_INVALID_SOURCE_TYPE_MESSAGE = 'Values of source type should be 0 or 1'

# Status / Status Codes
SEND_STATUS_CODE = 0
DELIVERY_STATUS_CODE = 6
SEND_STATUS = 'Success'
DELIVERY_STATUS = 'Success'


class returnValueSendSms(ComplexModel):
    __namespace__ = SMSGATEWAY_TARGET_NAMESPACE
    errorMsg = String
    status = Int
    msgIdArray = Long


class deliveryStatus(ComplexModel):
    __namespace__ = SMSGATEWAY_TARGET_NAMESPACE
    status = Int
    deliverDate = Int
    msgId = Long


class returnValueGetSmsDeliveryStatus(ComplexModel):
    __namespace__ = SMSGATEWAY_TARGET_NAMESPACE
    errorMsg = String
    status = Int
    reportItemArray = deliveryStatus


class respCode(ComplexModel):
    __namespace__ = SMSGATEWAY_TARGET_NAMESPACE
    respStatus = Int


class SMSGatewayException(Fault):
    __namespace__ = SMSGATEWAY_TARGET_NAMESPACE

    def __init__(self, message):
        super(SMSGatewayException, self).__init__(
            faultcode=SOAP_FAULT_CODE, faultstring=message,
            detail={SMSGATEWAY_EXCEPTION_TAG_NAME: SMSGATEWAY_TARGET_NAMESPACE})


class SDPSimulator(ServiceBase):
    # TODO: decide what to do, based on response type from config (OK, timeout, ...)
    # TODO: add faults for methods
    __service_name__ = SMSGATEWAY_SERVICE_NAME
    # __port_types__ = ({'name': 'SendSmsWebServiceImplPort', 'binding': 'tns:SendSmsWebServiceImplServiceSoapBinding'}, )

    # SDP
    # < wsdl:service name = "SendSmsWebServiceImplService" >
    #   < wsdl:port binding = "tns:SendSmsWebServiceImplServiceSoapBinding" name = "SendSmsWebServiceImplPort" >
    #       < soap:address location = "http://192.168.100.31:8181/smsgateway/sendsms" / >
    #   < / wsdl:port >
    # < / wsdl:service >

    # Simulator
    # < wsdl:service name = "SendSmsWebServiceImplService" >
    #   < wsdl:port name = "SendSmsWebService" binding = "tns:SendSmsWebService" >
    #       < soap:address location = "http://127.0.0.1:5000/smsgateway/services/SendSms/" / >
    #   < / wsdl:port >
    # < / wsdl:service >

    ###########################################################

    @rpc(Unicode(min_occurs=1, max_occurs='unbounded', nillable=False), Unicode(min_occurs=1, max_occurs='unbounded', nillable=False),
         Unicode(min_occurs=1, max_occurs='unbounded', nillable=False), Unicode(min_occurs=1, max_occurs='unbounded', nillable=False),
         Unicode(min_occurs=1, max_occurs='unbounded', nillable=False), Int(min_occurs=1, max_occurs='unbounded', nillable=False),
         Int(min_occurs=0, max_occurs='unbounded', nillable=True), Int(min_occurs=0, max_occurs='unbounded', nillable=True),
         _returns=returnValueSendSms.customize(sub_name='return'))
    def sendSms(ctx, sourceAddresses, destinationAddresses, msgBody, portNumber,
                msgEncoding, groupId, groupWeight, sourceType):

        # Normal Behaviour
        return SDPSimulator.sendSmsNormal(sourceAddresses, destinationAddresses, msgBody, portNumber,
                                          msgEncoding, groupId, groupWeight, sourceType)

    @staticmethod
    def sendSmsNormal(sourceAddresses, destinationAddresses, msgBody, portNumber,
                msgEncoding, groupId, groupWeight, sourceType):

        # Check if mandatory fields are present
        if sourceAddresses is None:
            return returnValueSendSms(errorMsg=SMSGATEWAY_MANDATORY_SOURCE_ADDRESS_MESSAGE, status=1)
        if destinationAddresses is None:
            return returnValueSendSms(errorMsg=SMSGATEWAY_MANDATORY_DESTINATION_ADDRESS_MESSAGE, status=1)
        if msgBody is None:
            return returnValueSendSms(errorMsg=SMSGATEWAY_MANDATORY_MESSAGE_BODY_MESSAGE, status=1)
        if portNumber is None:
            return SMSGatewayException(message=SOAP_FAULT_INTERNAL_ERROR_STRING)
        if portNumber != '0:0':
            return SMSGatewayException(message=SOAP_FAULT_INTERNAL_ERROR_STRING)
        if msgEncoding is None:
            return returnValueSendSms(errorMsg=SMSGATEWAY_MANDATORY_MESSAGE_ENCODING_MESSAGE, status=1)
        if groupId is None:
            return returnValueSendSms(errorMsg=SMSGATEWAY_MANDATORY_GROUP_ID_MESSAGE, status=1)

        # Check if fields' values are valid
        if type(msgEncoding) == int and int(msgEncoding) > 8:
            return returnValueSendSms(errorMsg=SMSGATEWAY_INVALID_MESSAGE_ENCODING_MESSAGE, status=1)
        if type(sourceType) == int and int(sourceType) not in [0, 1]:
            return returnValueSendSms(errorMsg=SMSGATEWAY_INVALID_SOURCE_TYPE_MESSAGE, status=1)
        if type(msgEncoding) != int or type(groupId) != int or type(groupWeight) != int or type(sourceType) != int:
            item_val = str(next(i for i in [msgEncoding, groupId, groupWeight, sourceType] if type(i) != int))
            return SMSGatewayException(message='%s %s' % (SOAP_INVALID_NUMBER_VALUE_MESSAGE, item_val))

        msg_id = random.choice(string.replace(string.digits, '0', '')) + \
            ''.join([random.choice(string.digits) for _ in range(11)])
        return returnValueSendSms(status=SEND_STATUS_CODE, msgId=msg_id)

    @rpc(Int, _returns=returnValueGetSmsDeliveryStatus.customize(sub_name='return'))
    def getSmsDeliveryStatus(ctx, msgIds):
        # Normal Behaviour
        return SDPSimulator.getSmsDeliveryStatusNormal(msgIds)

    @staticmethod
    def getSmsDeliveryStatusNormal(msgIds):

        # Check if mandatory fields are present
        if msgIds is None:
            return returnValueGetSmsDeliveryStatus(errorMsg=SMSGATEWAY_EMPTY_MESSAGE_ID_ARRAY_MESSAGE, status=1)

        # Check if fields' values are valid
        if re.match(r'^\d+$', str(msgIds)) is None:
            return SMSGatewayException(message='%s \"%s\"' % (SOAP_INVALID_STRING_VALUE_MESSAGE, str(msgIds)))

        deliver_date = str(int(time.time()))
        dest_address = random.choice(string.replace(string.digits, '0', '')) + \
            ''.join([random.choice(string.digits) for _ in range(11)])
        source_address = random.choice(string.replace(string.digits, '0', '')) + \
            ''.join([random.choice(string.digits) for _ in range(11)])
        report_items = deliveryStatus(deliverDate=deliver_date, destAddress=dest_address,
                                      msgId=msgIds, sourceAddress=source_address, status=DELIVERY_STATUS_CODE)
        result = returnValueGetSmsDeliveryStatus(status=0, reportItemArray=report_items)
        return result

    @rpc(Int, _returns=respCode)
    def setDeliveryStatusCode(ctx, statusCode):
        global DELIVERY_STATUS_CODE
        DELIVERY_STATUS_CODE = int(statusCode)
        return respCode(respStatus=0)

    @rpc(Int, _returns=respCode)
    def setSendStatusCode(ctx, statusCode):
        global SEND_STATUS_CODE
        SEND_STATUS_CODE = int(statusCode)
        return respCode(respStatus=0)

    @rpc(Int, _returns=respCode)
    def setSendStatus(ctx, status):
        global SEND_STATUS
        SEND_STATUS = status
        return respCode(respStatus=0)

    @rpc(Int, _returns=respCode)
    def setDeliveryStatus(ctx, status):
        global DELIVERY_STATUS
        DELIVERY_STATUS = status
        return respCode(respStatus=0)
