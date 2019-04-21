from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib.ticker as ticker
import matplotlib.dates as mdates

import textwrap
from adjustText import adjust_text

from datetime import date

from collections import OrderedDict

from DB_funcs import DATE_FROM
from DB_funcs import DATE_TO

date_from_ordinal = date.toordinal(DATE_FROM)
date_to_ordinal = date.toordinal(DATE_TO)

years       = mdates.YearLocator()


def set_x_axis_locator(ax, x_from, x_to):
    x_axis_range = x_to - x_from
    if x_axis_range < 300:
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
    elif x_axis_range < 4*365:
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    else:
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    return ax


def animate_multiple(i, ax, db, lines, frame_dates, franchise_text_array):
    n = 0
    cur_animation_day = frame_dates[i]
    max_gross_to_date = -1
    for franchise_data in db:
        to_index = min(franchise_date_pointer_array[n], len(franchise_data.gross_to_date_array)-1)
        while cur_animation_day > franchise_data.date_array[to_index]:
            franchise_date_pointer_array[n] = franchise_date_pointer_array[n] + 1
        x = franchise_data.date_array[0:to_index]
        y = franchise_data.gross_to_date_array[0:to_index]
        max_y = max(y) if to_index > 0 else -1
        if max_y > max_gross_to_date:
            max_gross_to_date = max_y
        lines[n].set_data(x, y)
        if len(y) > 0:
            film_name = textwrap.wrap(franchise_data.film_name_array[to_index-1], 14)
            franchise_text_array[n].set_text("\n".join(film_name))
            franchise_text_array[n].set_position((x[-1], y[-1]*1.05))
            # adjust_text(franchise_text_array)
        n = n + 1
    x_from  = date.toordinal(frame_dates[0]) - 10
    x_to    = max(date.toordinal(frame_dates[0]) + 100, date.toordinal(frame_dates[i]) + 40)
    ax.set_xlim(x_from, x_to)
    ax.set_ylim(0, max(max_gross_to_date*1.3, 0.7))
    ax = set_x_axis_locator(ax, x_from, x_to)
    ax.figure.canvas.draw()
    return lines


franchise_date_pointer_array = []


def create_date_array_for_animation(db):
    combined_dates = []
    for franchise_data in db:
        combined_dates = combined_dates + franchise_data.date_array
    unique_dates = list(OrderedDict.fromkeys(combined_dates))
    sorted_unique_dates = sorted(unique_dates)
    return sorted_unique_dates


def create_animation_from_db(db):
    my_dpi = 150
    # fig = plt.figure(figsize=(1920/my_dpi, 1080/my_dpi), dpi=my_dpi)
    fig = plt.figure(figsize=(1080/my_dpi, 720/my_dpi), dpi=my_dpi)
    # fig = plt.figure()
    plt.title("Franchise Earnings Comparison Over 20 Years")
    frame_dates = create_date_array_for_animation(db)
    yformat = ticker.FormatStrFormatter("$%2.1fB")
    ax = plt.gca()
    ax.yaxis.set_major_formatter(yformat)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    lines = []
    handles = []
    franchise_text_array = []
    my_bbox = dict(boxstyle="round")
    for _ in db:
        line, = ax.step([], [], lw=1, where='post')
        lines.append(line)
        handles.append(line)
        franchise_date_pointer_array.append(0)
        # franchise_text_array.append(ax.text(0, 0, "Oops", rotation=-45, horizontalalignment='center'))
        # franchise_text_array.append(ax.text(0, 0, "", horizontalalignment='center', fontsize=6, bbox=my_bbox))
        franchise_text_array.append(ax.text(0, 0, "", horizontalalignment='center', fontsize=6))
    plt.legend(handles, [x.franchise_name for x in db], loc='upper left', fontsize=6)
    print("There are %s dates in frame_dates array" % len(frame_dates))
    animation_time = len(frame_dates)/30
    print("Which will make a video %.2f seconds long" % animation_time)
    anim = animation.FuncAnimation(fig,
                                   animate_multiple,
                                   fargs=(ax, db, lines, frame_dates, franchise_text_array),
                                   frames=int(len(frame_dates[:])*1.2), interval=0.01, blit=True)
    # anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
    plt.show()
