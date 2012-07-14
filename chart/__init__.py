#!/usr/bin/env python
# -*- coding: utf-8 -*-

# filename   : __init__.py
# created at : 2012年07月14日 星期六 22时10分19秒
# author     : Jianing Yang <jianingy.yang AT gmail DOT com>

__author__ = 'Jianing Yang <jianingy.yang AT gmail DOT com>'

from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.ticker import FormatStrFormatter
from matplotlib.dates import DateFormatter
from cStringIO import StringIO
import matplotlib.pyplot as plt

from matplotlib.ticker import AutoMinorLocator


def create_chart(width, height):
    fig = plt.figure(figsize=(width, height), dpi=96)
    ax = fig.add_axes([0.02, 0.2, 0.8, 0.75], frame_on=False)
    ax.get_frame().set_linewidth(5)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('right')
    ax.tick_params(direction='out', width=0.5, length=5, pad=4,
                   labelsize=7)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%2.5f'))
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M'))

    fig.autofmt_xdate()

    return (fig, ax)


def output_chart(chart):
    fig, ax = chart[:2]
    ax.autoscale_view()

    xmin, xmax = ax.get_xaxis().get_view_interval()
    ymin, ymax = ax.get_yaxis().get_view_interval()

    args = dict(color='black', linewidth=2)
    ax.add_artist(Line2D((xmin, xmax), (ymin, ymin), **args))
    ax.add_artist(Line2D((xmax, xmax), (ymin, ymax), **args))
    args = dict(color='black', linewidth=1)
    ax.add_artist(Line2D((xmin, xmax), (ymax, ymax), **args))
    ax.add_artist(Line2D((xmin, xmin), (ymin, ymax), **args))

    ax.get_xaxis().set_minor_locator(AutoMinorLocator())

    ax.get_xaxis().grid(which='both', color='#999999',
                        linestyle=':', linewidth=0.5)
    ax.get_yaxis().grid(which='both', color='#999999',
                        linestyle=':', linewidth=0.5)

    output = StringIO()
    plt.savefig(output, format='png')

    return output.getvalue()


def candlestick(chart, quotes, colorup='#00ff00', colordown='#ff0000'):
    fig, ax = chart[:2]

    start = quotes[0][0]
    end = quotes[-1][0]

    width = (end - start) / len(quotes) * 0.7

    start = ((start) / 300) * 300
    end = ((end) / 300) * 300

    ax.set_xlim([start, end])

    offset = width / 2.0
    stick_width = 0.5

    for quote in quotes:

        ts, opening, closing, high, low = quote[:5]

        if closing < opening:
            height = round(opening - closing, 5)
            bottom = closing
            color = colordown
        else:
            height = round(closing - opening, 5)
            bottom = opening
            color = colorup

        stick = Line2D(
            xdata=(ts, ts), ydata=(low, high),
            color='k',
            linewidth=stick_width,
            antialiased=False,
            zorder=5,
        )

        candle = Rectangle(
            xy=(ts - offset, bottom),
            width=width,
            height=height,
            facecolor=color,
            edgecolor='k',
            zorder=10,
            antialiased=False,
        )
        ax.add_line(stick)
        ax.add_patch(candle)
        #ax.bar(ts, height, width, bottom, color=color, edgecolor='k',
        #       zorder=10, antialiased=False, align='center')
