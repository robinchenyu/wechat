import hashlib
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def wx_sign(req):
        TOKEN="robinchenyu02528359"
        signature = req.GET.get('signature')
        timestamp = req.GET.get('timestamp')
        nonce = req.GET.get('nonce')

        if not signature or not timestamp or not nonce:
                return HttpResponse("get param failed")

        tmpArr = [TOKEN, timestamp, nonce]
        tmpArr = sorted(tmpArr)
        tmpStr = "".join(tmpArr)
        sha = hashlib.sha1()
        sha.update(tmpStr)

        if (sha.hexdigest() == signature):
                return HttpResponse(req.GET.get('echostr'))
        else:
                return HttpResponse("failed signature {} sum {}" % (type(signature), sha.hexdigest()))
