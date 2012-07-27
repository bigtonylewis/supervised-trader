#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename   : gartley.py
# created at : 2012年07月27日 星期五 14时27分44秒
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'

from indicators.trend import swing_zz

def ab_eq_cd(ticks, deviation=0.0005, spread=0.0025):
    zigzags, = swing_zz(ticks, span=12, backtrace=24, debug=0)
    last = zigzags[-5:]

    if len(last) < 5:
        return None

    xa = abs(last[0][3] - last[1][3])
    ab = abs(last[1][3] - last[2][3])
    bc = abs(last[2][3] - last[3][3])
    cd = abs(last[3][3] - last[4][3])

    if cd < spread:
        return None

    if ab / xa - 0.618 >= deviation:
        return None

    if cd / xa - 0.786 >= deviation:
        return None

    if bc / ab - 0.382 < deviation:
        if cd / bc - 1.272 >= deviation:
            return None
    elif bc / ab - 0.886 < deviation:
        if cd / bc - 1.618 >= deviation:
            return None
    else:
        return None


    return last
