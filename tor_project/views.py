import logging
import time
import hashlib

import tornado.web
from xmlparse import parse_xml


logger = logging.getLogger(__name__)


class WechatHandler(tornado.web.RequestHandler):
    TOKEN = "robinchenyu02528359"

    def get(self):
        if not self._check_sign():
            return self.write("check_sign failed")

        greeting = self.get_argument('greeting', 'Hello')
        self.write(greeting + ', friendly user!')

    def post(self):
        if not self._check_sign():
            return self.write("post check sign failed")

        data1 = parse_xml(self.request.body)
        logger.info("log done")

        logger.info(data1)
        data1['CreateTime'] = int(time.time())
        logger.info("post resp")
        self.set_header('Content-Type', "application/xml")

        return self._render_msg1('msg/%s_msg.xml' % data1.get('MsgType'), data1)

    def _render_msg1(self, template, kwargs):
        msg = ''
        try:
            with open(template, 'r') as fr:
                msg = fr.read()
        except Exception as e:
            logger.error("read template %s failed: %s" % (template, e.message))
            pass
        msg = msg.format(**kwargs)
        # logger.info("msg: %s" % msg)
        return self.write(msg)

    def _check_sign(self):
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        if not signature or not timestamp or not nonce:
            logger.error("cant get signature or timestamp or nonce")
            return False

        tmpArr = [self.TOKEN, timestamp, nonce]
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
