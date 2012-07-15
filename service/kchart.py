#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename   : kchart.py
# created at : 2012年07月14日 星期六 10时44分51秒
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'

from twisted.internet import reactor, defer
from twisted.internet.threads import deferToThread
from twisted.python import log
from matplotlib.dates import date2num
from datetime import datetime
from txpostgres import txpostgres
from service.base import BaseResource
from chart import create_chart, output_chart, candlestick
from chart.trend import moving_average

import re
import time
import logging


TIME_RE = re.compile(
    '(?P<oper>[-+])?(?P<amount>\d+)(?P<unit>[smhdw])'
    '|(?P<datetime>\d+-\d+-\d+ \d+:\d+:\d+)'
    '|(?P<now>now)')
DSN = 'host=localhost port=5432 user=jianingy dbname=jianingy'
TIME_UNIT = dict(s=1, m=60, h=3600, d=86400, w=86400 * 7)


class InvalidChartData(Exception):
    pass


def to_timestamp(matched):
    c = matched.groupdict()
    if c['now'] == 'now':
        return time.time()
    ts = float(c['amount']) * TIME_UNIT[c['unit']]
    if c['oper'] == '-':
        return time.time() - ts
    else:
        return time.time() + ts


class KChartService(BaseResource):

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
    def _fetch(self, cursor, option):
        tbl = "kchart_%s_%sm" % (option['symbol'].lower(), option['period'])
        sql = "SELECT extract(EPOCH FROM ts), open, close, high, low "
        sql += "FROM %s " % tbl
        sql += "WHERE ts >= to_timestamp(%(start)s) "
        sql += "AND ts <= to_timestamp(%(end)s) ORDER BY ts"
        iterator = yield cursor.execute(sql, option)

        # convert unix timestamp to ordinal timestamp
        ticks = map(lambda x: (date2num(datetime.fromtimestamp(x[0])),
                               x[1], x[2], x[3], x[4]), iterator.fetchall())

        defer.returnValue(ticks)

    def _draw(self, ticks):
        chart = create_chart(12.8, 4.8)
        candlestick(chart, ticks)
        args = dict(color='grey', type='ema', width=0.5)
        moving_average(chart, ticks, n=5, **args)
        moving_average(chart, ticks, n=8, **args)
        moving_average(chart, ticks, n=13, **args)
        moving_average(chart, ticks, n=21, **args)
        moving_average(chart, ticks, n=34, **args)
        moving_average(chart, ticks, n=55, **args)
        return output_chart(chart)

    @defer.inlineCallbacks
    def async_GET(self, request):

        option = dict()
        option['start'] = request.args.get('start', ['-8h'])[0]
        option['end'] = request.args.get('end', ['now'])[0]
        option['period'] = request.args.get('peroid', ['1'])[0]
        option['symbol'] = request.args.get('symbol', ['eurusd'])[0]

        matched = TIME_RE.match(option['start'])
        if not matched:
            raise InvalidChartData('start time is invalid')
        else:
            option['start'] = to_timestamp(matched)

        matched = TIME_RE.match(option['end'])
        if not matched:
            raise InvalidChartData('end time is invalid')
        else:
            option['end'] = to_timestamp(matched)

        ticks = yield self.db.runInteraction(self._fetch, option)
        result = yield deferToThread(self._draw, ticks)
        request.setHeader('Content-Type', 'image/png')
        defer.returnValue(result)
