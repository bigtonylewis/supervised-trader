#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename   : kinput.py
# created at : 2012年07月13日 星期五 13时55分11秒
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'

from twisted.internet import reactor, defer
from twisted.python import log
from txpostgres import txpostgres
from base import BaseResource
import psycopg2
import logging

DSN = 'host=localhost port=5432 user=jianingy dbname=jianingy'


class InvalidCandleData(Exception):
    pass


class KInputService(BaseResource):

    def __init__(self, *args, **kwargs):
        self._database_connected = False
        self.db = txpostgres.ConnectionPool(None, DSN)
        d = self.db.start()
        d.addBoth(self._connect_database)

        BaseResource.__init__(self, *args, **kwargs)

    def _connect_database(self, ignore):
        from twisted.python.failure import Failure

        if isinstance(ignore, Failure):
            log.msg("cannot connect database", level=logging.ERROR)
            log.msg(ignore.getTraceback(), level=logging.ERROR)
            reactor.stop()
        else:
            self._database_connected = True

    @defer.inlineCallbacks
    def _save(self, cursor, candle):

        tbl = "kchart_%s_%sm" % (candle['symbol'].lower(), candle['period'])
        sql = "INSERT INTO %s(ts, open, close, high, low, volume) " % tbl
        sql += """VALUES(to_timestamp(%(time)s),
%(open)s, %(close)s, %(high)s, %(low)s, %(volume)s);"""

        yield cursor.execute(sql, candle)
        defer.returnValue(dict(success=True, affected=cursor.rowcount))

    @defer.inlineCallbacks
    def async_GET(self, request):

        names = ('symbol', 'period', 'time',
                 'open', 'close', 'high', 'low', 'volume')
        candle = dict()
        for name in names:
            candle[name] = request.args.get(name, [None])[0]
            if not candle[name]:
                raise InvalidCandleData('%s is empty' % name)
        try:
            result = yield self.db.runInteraction(self._save, candle)
            defer.returnValue(result)
        except psycopg2.IntegrityError:
            log.msg("duplicate candle found %s" % candle,
                    level=logging.WARNING)
            defer.returnValue(dict(success=True,
                                   affected=0, reason="duplicate"))
