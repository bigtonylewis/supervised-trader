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

import re
import time
import logging


TIME_RE = re.compile(
    '(?P<oper>[-+])?(?P<amount>\d+)(?P<unit>[smhdw])'
    '|(?P<datetime>\d+-\d+-\d+ \d+:\d+:\d+)'
    '|(?P<now>now)')
DSN = 'host=guru.corp.linuxnote.net port=5432 user=jianingy dbname=forex password=zzzz'
TIME_UNIT = dict(s=1, m=60, h=3600, d=86400, w=86400 * 7)


class InvalidChartData(Exception):
    pass


def to_timestamp(matched, base=time.time()):
    c = matched.groupdict()
    if c['now'] == 'now':
        return time.time()
    if c['datetime']:
        return time.mktime(time.strptime(c['datetime'],
                                         '%Y-%m-%d %H:%M:%S'))
    ts = float(c['amount']) * TIME_UNIT[c['unit']]
    if c['oper'] == '-':
        return base - ts
    else:
        return base + ts


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

    @defer.inlineCallbacks
    def _draw(self, option):

        # get more data
        preload = 89
        unit = int(option['period']) * 60
        option['view_start'] = option['start']
        option['view_end'] = option['end'] + 3 * unit
        option['start'] -= preload * unit
        ticks = yield self.db.runInteraction(self._fetch, option)
        chart = create_chart(6.4, 3.0)
        candlestick(chart, ticks)

        from chart.trend import swing_zz
        from chart.trend import moving_average

        if int(option['period']) == 1:
            args = dict(span=12, backtrace=24)
        elif int(option['period']) == 5:
            args = dict(span=12, backtrace=24)
        elif int(option['period']) == 60:
            args = dict(span=12, backtrace=24)

        swing_zz(chart, ticks, **args)

        args = dict(color='#cccccc', type='ema', width=0.5)
        moving_average(chart, ticks, n=5, **args)
        moving_average(chart, ticks, n=8, **args)
        moving_average(chart, ticks, n=13, **args)
        moving_average(chart, ticks, n=21, **args)
        moving_average(chart, ticks, n=34, **args)
        moving_average(chart, ticks, n=55, **args)

        from spectators import gartley
        for shift in xrange(preload + 1, len(ticks)):
            result = gartley.ab_eq_cd(ticks[shift:])
            if result:
                fig, ax = chart
                xs = map(lambda x: x[2], filter(lambda x: x, result))
                ys = map(lambda x: x[3], filter(lambda x: x, result))
                ax.plot(xs, ys, color='r', lw=1)
                break

        defer.returnValue(output_chart(chart, option))

    @defer.inlineCallbacks
    def async_GET(self, request):

        option = dict()
        option['start'] = request.args.get('start', ['-8h'])[0]
        option['end'] = request.args.get('end', ['now'])[0]
        option['period'] = request.args.get('period', ['1'])[0]
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
            option['end'] = to_timestamp(matched, option['start'])

        result = yield self._draw(option)
        request.setHeader('Content-Type', 'image/png')
        defer.returnValue(result)
