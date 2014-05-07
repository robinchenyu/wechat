import tornado.web
import logging

logger = logging.getLogger(__name__)

class WechatHandler(tornado.web.RequestHandler):
    TOKEN="robinchenyu02528359"
    def get(self):
        if not self._check_sign():
            return self.write("check_sign failed")

        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')

    def post(self):
        if not self._check_sign():
            return self.write("post check sign failed")

        import xml.etree.ElementTree as ET
        data1 = {}
        for t, element in ET.iterparse(req):
            data1[element.tag] = smart_str(element.text)
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

        logger.info( "post resp" )
        self.set_header(content_type = "application/xml")
        return self.write(repMsg)


    def _check_sign(self):
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
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
