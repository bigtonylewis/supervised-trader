#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename   : trend.py<2>
# created at : 2012年07月14日 星期六 23时29分19秒
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'

from indicators.trend import moving_average as _moving_average


def moving_average(chart, ticks, n=5, color='blue', width=1):
    fig, ax = chart[:2]
    ma = _moving_average(map(lambda x: x[2], ticks), n)
    linema20, = ax.plot(map(lambda x: x[0], ticks),
                        ma, color='blue',
                        lw=width, label='MA (%d)' % n)
