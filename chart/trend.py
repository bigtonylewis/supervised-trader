#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename   : trend.py<2>
# created at : 2012年07月14日 星期六 23时29分19秒
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'


def moving_average(chart, ticks, n=5, color='blue', width=1, type='simple',
                   start=0, end=-1):
    from indicators.trend import moving_average as _moving_average
    fig, ax = chart[:2]
    ma = _moving_average(map(lambda x: x[2], ticks), n, type=type)[start:end]
    linema20, = ax.plot(map(lambda x: x[0], ticks[start:end]),
                        ma, color=color,
                        lw=width, label='MA (%d)' % n)


def swing_zz(chart, ticks, color='blue', start=0, span=6, backtrace=3,
             debug=0):
    from indicators.trend import swing_zz as _swing_zz

    fig, ax = chart
    lows, highs, zigzags = _swing_zz(ticks)

    if debug == 2:
        xs = map(lambda x: x[1][0], filter(lambda x: x, lows))
        ys = map(lambda x: x[1][4], filter(lambda x: x, lows))
        ax.plot(xs, ys, 'bo', lw=0.5, label='SW')

        xs = map(lambda x: x[1][0], filter(lambda x: x, highs))
        ys = map(lambda x: x[1][3], filter(lambda x: x, highs))
        ax.plot(xs, ys, 'ro', lw=0.5, label='SW')

    elif debug == 1:
        xs = map(lambda x: x[2], filter(lambda x: x[0] == 0, zigzags))
        ys = map(lambda x: x[3], filter(lambda x: x[0] == 0, zigzags))
        ax.plot(xs, ys, 'bo', lw=0.5, label='SW')

        xs = map(lambda x: x[2], filter(lambda x: x[0] == 1, zigzags))
        ys = map(lambda x: x[3], filter(lambda x: x[0] == 1, zigzags))
        ax.plot(xs, ys, 'ro', lw=0.5, label='SW')

    xs = map(lambda x: x[2], filter(lambda x: x, zigzags))
    ys = map(lambda x: x[3], filter(lambda x: x, zigzags))
    ax.plot(xs, ys, color, lw=0.5)
