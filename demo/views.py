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
        return False

    tmpArr = [TOKEN, timestamp, nonce]
    tmpArr = sorted(tmpArr)
    tmpStr = "".join(tmpArr)
    sha = hashlib.sha1()
    sha.update(tmpStr)

    if (sha.hexdigest() == signature):
        return True
    else:
        logger.info("check signature failed {} {} {} {}" % (signature, timestamp, nonce, sha.hexdigest()))
        return False

@csrf_exempt
def wx_sign(req):
    if not check_sign(req):
        return HttpResponse("failed")

    if req.method == "GET":
        logger.info( "get method")
        return HttpResponse(req.GET.get('echostr'))
    else:
        logger.info( "post method " )

        import xml.etree.ElementTree as ET
        for element in ET.iterparse(req):
            logger.info("{} -- {}" % (element.tag, element.text))
        logger.info( "log done" )

        logger.info( req.GET)
