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
from matplotlib.dates import date2num
from datetime import datetime
from cStringIO import StringIO
import matplotlib.pyplot as plt




def create_chart(width, height):
    fig = plt.figure(figsize=(width, height))
    ax = fig.add_axes([0.02, 0.2, 0.8, 0.75], frame_on=False)
    ax.get_frame().set_linewidth(5)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('right')
    ax.tick_params(direction='out', width=0.5, length=2, pad=4,
                   labelsize=2.5)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%2.5f'))
    ax.xaxis.set_major_formatter(DateFormatter('%b %d %H:%M'))

    #    fig.autofmt_xdate()

    return (fig, ax)


def output_chart(chart, option):
    fig, ax = chart[:2]
    #ax.autoscale_view()

    xmin = date2num(datetime.fromtimestamp(option['view_start']))
    xmax = date2num(datetime.fromtimestamp(option['view_end']))
    ax.get_xaxis().set_view_interval(xmin, xmax, ignore=True)

    xmin, xmax = ax.get_xaxis().get_view_interval()
    ymin, ymax = ax.get_yaxis().get_view_interval()

    args = dict(color='black', linewidth=2)
    ax.add_artist(Line2D((xmin, xmax), (ymin, ymin), **args))
    ax.add_artist(Line2D((xmax, xmax), (ymin, ymax), **args))
    args = dict(color='black', linewidth=1)
    ax.add_artist(Line2D((xmin, xmax), (ymax, ymax), **args))
    ax.add_artist(Line2D((xmin, xmin), (ymin, ymax), **args))

    from matplotlib.dates import MinuteLocator

    locator = MinuteLocator(interval=int((option['view_end'] - option['view_start']) / 60 / 14))
    ax.get_xaxis().set_major_locator(locator)
    locator = MinuteLocator(interval=int((option['view_end'] - option['view_start']) / 60 / 14 / 2))
    ax.get_xaxis().set_minor_locator(locator)

    ax.get_xaxis().grid(which='both', color='#999999',
                        linestyle=':', lw=0.3)
    ax.get_yaxis().grid(which='both', color='#999999',
                        linestyle=':', lw=0.3)

    output = StringIO()
    plt.savefig(output, format='png', dpi=300)

    return output.getvalue()


def candlestick(chart, quotes, colorup='#00ff00', colordown='#ff0000'):
    fig, ax = chart[:2]

    start = quotes[0][0]
    end = quotes[-1][0]

    width = (end - start) / len(quotes) * 0.6

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
            antialiased=True,
            zorder=5,
        )

        candle = Rectangle(
            xy=(ts - offset, bottom),
            width=width,
            height=height,
            facecolor=color,
            edgecolor='#333333',
            lw=0.5,
            zorder=10,
            antialiased=True,
        )
        ax.add_line(stick)
        ax.add_patch(candle)
        #ax.bar(ts, height, width, bottom, color=color, edgecolor='k',
        #       zorder=10, antialiased=False, align='center')
