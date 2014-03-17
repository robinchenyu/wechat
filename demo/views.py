import hashlib
from django.shortcuts import render
from django.http import HttpResponse
import logging
logger = logging.getLogger(__name__)
# Create your views here.
def check_sign(signature, timestamp, nonce):

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
                return False

def wx_sign(req):
        TOKEN="robinchenyu02528359"
        if req.method == "GET":
                logger.info( "get method")
                signature = req.GET.get('signature')
                timestamp = req.GET.get('timestamp')
                nonce = req.GET.get('nonce')
                if check_sign(signature, timestamp, nonce):
                        return HttpResponse(req.GET.get('echostr'))
        else:
                logger.info( "post method")
                signature = req.POST.get('signature')
                timestamp = req.POST.get('timestamp')
                nonce = req.POST.get('nonce')

                if check_sign(signature, timestamp, nonce):
                        logger.info( "msg check ok! {} " % req.POST)
                        logger.info( "body {} " % req.body)
                        logger.info( "meta {} " % req.META)

                        for line in req.xreadlines():
                                logger.info( "line: {} " % line)
