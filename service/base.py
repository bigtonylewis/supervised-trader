#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename   : base.py
# created at : 2012年07月13日 星期五 13时47分36秒
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'

from twisted.web.resource import Resource
from twisted.web.server import NOT_DONE_YET
from twisted.internet import defer
from twisted.python.failure import Failure
from twisted.python import log
from ujson import encode as json_encode
import logging


class NotImplement(Exception):
    pass


class BaseResource(Resource):

    isLeaf = True

    def cancel(self, err, d):
        log.msg("Cancelling current request.", levenl=logging.DEBUG)
        d.cancel()

    def finalize(self, value, request):

        if isinstance(value, Failure):
            request.setResponseCode(500)
            response = dict(success=False,
                            reason=value.getErrorMessage(),
                            traceback=value.getTraceback())
        else:
            response = value
            request.setResponseCode(200)

        if isinstance(response, str):
            request.write(response)
        elif isinstance(response, unicode):
            request.write(response.decode('UTF-8'))
        else:
            request.setHeader('Content-Type',
                              'application/json; charset=UTF-8')
            request.write(json_encode(response))

        request.finish()

    def render_GET(self, request):
        d = self.async_GET(request)
        request.notifyFinish().addErrback(self.cancel, d)
        d.addBoth(self.finalize, request)
        return NOT_DONE_YET

    def async_GET(self, request):
        raise NotImplement()
