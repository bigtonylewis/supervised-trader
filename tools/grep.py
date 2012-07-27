#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename   : grep.py
# created at : 2012年07月27日 星期五 15时48分46秒
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'

period = '5'

import psycopg2
conn_string = "host=guru.corp.linuxnote.net user=jianingy password=zzzz dbname=forex"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
cursor.execute("SELECT extract(EPOCH FROM ts), open, close, high, low from kchart_eurusd_%sm" % period)
records = cursor.fetchall()

from indicators.trend import swing_zz
from spectators.gartley import ab_eq_cd

import time

span = 89
fmt = '%Y-%m-%d+%H:%M:%S'
for shift in xrange(0, len(records) - span):
    result = ab_eq_cd(records[shift:shift + span])
    if result:
        print result
        end_time = time.strftime(fmt, time.localtime(result[0][2] + 89 * int(period) * 60))
        start_time = time.strftime(fmt, time.localtime(result[0][2]))
        print "http://localhost:8080/?period=%s&start=%s&end=%s" % (period, start_time, end_time)
