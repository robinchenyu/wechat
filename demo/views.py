import time
import hashlib
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging
logger = logging.getLogger(__name__)
# Create your views here.
def check_sign(req):
    TOKEN="robinchenyu02528359"
    signature = req.GET.get('signature')
    timestamp = req.GET.get('timestamp')
    nonce = req.GET.get('nonce')
    if not signature or not timestamp or not nonce:
        logger.error("cant get signature or timestamp or nonce")
        return False

    tmpArr = [TOKEN, timestamp, nonce]
    tmpArr = sorted(tmpArr)
    tmpStr = "".join(tmpArr)
    sha = hashlib.sha1()
    sha.update(tmpStr)

    if (sha.hexdigest() == signature):
        logger.info("check signature success!")
        return True
    else:
        logger.info("check signature failed {} {} {} {}".format(signature, timestamp, nonce, sha.hexdigest()))
        return False

@csrf_exempt
def wx_sign(req):
    if not check_sign(req):
        return HttpResponse("check_sign failed")

    if req.method == "GET":
        logger.info( "get method")
        return HttpResponse(req.GET.get('echostr'))
    else:
        logger.info( "post method " )

        import xml.etree.ElementTree as ET
        data1 = {}
        for t, element in ET.iterparse(req):
            data1[element.tag] = element.text
        logger.info( "log done" )

        logger.info(data1)
        data1['CreateTime'] = int(time.time())
        if data1['MsgType'] == 'text':
            repMsg = """<xml>
            <ToUserName><![CDATA[{FromUserName}]]></ToUserName>
            <FromUserName><![CDATA[{ToUserName}]]></FromUserName>
            <CreateTime>{CreateTime}</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{Content}]]></Content>
            </xml>""".format(**data1)
        elif data1['MsgType'] == 'event':
            repMsg = """<xml>
            <ToUserName><![CDATA[{FromUserName}]]></ToUserName>
            <FromUserName><![CDATA[{ToUserName}]]></FromUserName>
            <CreateTime>{CreateTime}</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[welcome]]></Content>
            </xml>""".format(**data1)


        logger.info( req.GET)
        return HttpResponse(repMsg, content_type="application/xml")
