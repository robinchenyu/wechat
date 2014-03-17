import hashlib
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging
logger = logging.getLogger(__name__)
# Create your views here.
def check_sign(signature, timestamp, nonce):
    TOKEN="robinchenyu02528359"
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
    if req.method == "GET":
        logger.info( "get method")
        signature = req.GET.get('signature')
        timestamp = req.GET.get('timestamp')
        nonce = req.GET.get('nonce')
        if check_sign(signature, timestamp, nonce):
            return HttpResponse(req.GET.get('echostr'))
    else:
        logger.info( "post method {} {}" % (req.GET, req.POST))
        signature = req.POST.get('signature')
        timestamp = req.POST.get('timestamp')
        nonce = req.POST.get('nonce')

        if check_sign(signature, timestamp, nonce):
            logger.info( "msg check ok! {} " % req.POST)
            logger.info( "body {} " % req.body)
            logger.info( "meta {} " % req.META)

            for line in req.xreadlines():
                logger.info( "line: {} " % line)
