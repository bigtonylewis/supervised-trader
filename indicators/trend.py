#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename   : trend.py
# created at : 2012年07月14日 星期六 23时27分57秒
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'
import numpy as np


def moving_average(x, n, type='simple'):

    """
    compute an n period moving average.

    type is 'simple' | 'exponential'

    """
    x = np.asarray(x)
    if type == 'simple':
        weights = np.ones(n)
    else:
        weights = np.exp(np.linspace(-1., 0., n))

    weights /= weights.sum()
    a = np.convolve(x, weights, mode='full')[:len(x)]
    a[:n] = a[n]
    return a


def swing_zz(ticks, span=6, backtrace=3, debug=0):

    lows, highs, zigzags = list(), list(), list()
    last_low, last_high = None, None
    for shift in xrange(0, len(ticks)):

        # find lows
        val = min(zip(range(shift, shift + span), ticks[shift:shift + span]),
                  key=lambda x: x[1][4])

        while lows and val[0] - lows[-1][0] < backtrace:
            last_low = lows.pop()
            if val[1][4] > last_low[1][4]:
                val = last_low
                break

        lows.append(val)

        # find highs
        val = max(zip(range(shift, shift + span), ticks[shift:shift + span]),
                  key=lambda x: x[1][3])

        while highs and val[0] - highs[-1][0] < backtrace:
            last_high = highs.pop()
            if val[1][3] < last_high[1][3]:
                val = last_high
                break

        highs.append(val)


    if debug > 1:
        _lows, _highs = list(lows), list(highs)

    # cut & merge
    lows.reverse()
    highs.reverse()
    while lows and highs:
        if lows[-1] < highs[-1]:
            low = lows.pop()
            if zigzags and zigzags[-1][0] == 0:
                if zigzags[-1][3] > low[1][4]:
                    zigzags.pop()
                    zigzags.append((0, low[0], low[1][0], low[1][4]))
            else:
                zigzags.append((0, low[0], low[1][0], low[1][4]))
        else:
            high = highs.pop()
            if zigzags and zigzags[-1][0] == 1:
                if zigzags[-1][3] < high[1][3]:
                    zigzags.pop()
                    zigzags.append((1, high[0], high[1][0], high[1][3]))
            else:
                zigzags.append((1, high[0], high[1][0], high[1][3]))

    # deal with the lasts
    if lows:
        low = min(lows, key=lambda x: x[1][4])
        if zigzags and zigzags[-1][0] == 0:
            if zigzags[-1][3] > low[1][4]:
                zigzags.pop()
                zigzags.append((0, low[0], low[1][0], low[1][4]))
        else:
            zigzags.append((0, low[0], low[1][0], low[1][4]))
    elif highs:
        high = min(highs, key=lambda x: x[1][3])
        if zigzags and zigzags[-1][0] == 1:
            if zigzags[-1][3] < high[1][3]:
                zigzags.pop()
                zigzags.append((1, high[0], high[1][0], high[1][3]))
        else:
            zigzags.append((1, high[0], high[1][0], high[1][3]))

    if debug > 1:
        return (zigzags, _lows, _highs)
    else:
        return (zigzags,)


def swing_points(ticks, start=0):
    """Inspired by http://codebase.mql4.com/source/1367"""

    depth = 6
    deviation = 0.0005
    backstep = 3

    shift, last_low, last_high = depth, 0.0, 0.0
    buffer_high, buffer_low = [0.0] * len(ticks), [0.0] * len(ticks)
    result = [0.0] * len(ticks)

    for shift, tick in enumerate(ticks):

        if shift < depth:
            continue

        ts, open, close, high, low = tick

        # low
        val = min(map(lambda x: x[4], ticks[shift - depth:shift]))
        if val == last_low:
            val = 0.0
        else:
            last_low = val
            if low - val > deviation:
                val = 0.0
            else:
                for back in xrange(1, backstep + 1):
                    res = buffer_low[shift - back]
                    if res != 0.0 and res > val:
                        buffer_low[shift - back] = 0.0

        buffer_low[shift] = val

        # high
        val = max(map(lambda x: x[3], ticks[shift - depth:shift]))
        if val == last_high:
            val = 0.0
        else:
            last_high = val
            if val - high > deviation:
                val = 0.0
            else:
                for back in xrange(1, backstep + 1):
                    res = buffer_high[shift - back]
                    if res != 0.0 and res < val:
                        buffer_high[shift - back] = 0.0

        buffer_high[shift] = val

     # cutting
    lasthigh, lastlow = -1, -1
    lasthigh_pos, lastlow_pos = -1, -1

    for shift, tick in enumerate(ticks):

        if shift < depth:
            continue

        ts, open, close, high, low = tick

        curlow = buffer_low[shift]
        curhigh = buffer_high[shift]

        if curlow == 0 and curhigh == 0:
            continue

        if curhigh != 0:
            if lasthigh > 0:
                if lasthigh < curhigh:
                    buffer_high[lasthigh_pos] = 0
                else:
                    buffer_high[shift] = 0
            if lasthigh < curhigh or lasthigh < 0:
                lasthigh = curhigh
                lasthigh_pos = shift

            lastlow = -1

        if curlow != 0:
            if lastlow > 0:
                if lastlow > curlow:
                    buffer_low[lastlow_pos] = 0
                else:
                    buffer_low[shift ] = 0
            if curlow < lastlow or lastlow < 0:
                lastlow = curlow
                lastlow_pos = shift

            lasthigh = -1

    for shift in xrange(0, len(buffer_low)):

        if shift < depth:
            buffer_low[shift] = 0.0
        else:
            res = buffer_high[shift]
            if res != 0:
                buffer_low[shift] = res

        result[shift] = buffer_low[shift]

    return result
